from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from lang import EN, FA, get_lang
from utils import fetch_prices


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    args = context.args
    if not args:
        await update.message.reply_text(t["price_usage"], parse_mode="Markdown")
        return

    try:
        data = fetch_prices(args)
    except Exception:
        await update.message.reply_text(t["price_error"])
        return

    if not data:
        await update.message.reply_text(t["price_none"])
        return

    lines = [t["live_prices"]]
    for coin_id, info in data.items():
        price_usd = info.get("usd", 0)
        change = info.get("usd_24h_change")
        change_str = f"{change:+.2f}%" if change else "N/A"
        icon = "🟢" if change and change >= 0 else "🔴"
        lines.append(f"{icon} *{coin_id.title()}*: `${price_usd:,.2f}` _{change_str}_")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    args = context.args
    if len(args) < 3:
        await update.message.reply_text(t["alert_usage"], parse_mode="Markdown")
        return

    coin, direction, target_str = args[0].lower(), args[1].lower(), args[2]
    if direction not in ("above", "below"):
        await update.message.reply_text(t["alert_direction"], parse_mode="Markdown")
        return

    try:
        target = float(target_str)
    except ValueError:
        await update.message.reply_text(t["alert_invalid"])
        return

    try:
        data = fetch_prices([coin])
    except Exception:
        await update.message.reply_text(t["alert_error"])
        return

    if coin not in data:
        await update.message.reply_text(t["alert_not_found"].format(coin), parse_mode="Markdown")
        return

    current = data[coin]["usd"]
    triggered = (direction == "above" and current > target) or (
        direction == "below" and current < target
    )

    if triggered:
        await update.message.reply_text(
            t["alert_triggered"].format(coin.title(), current, direction, target),
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            t["alert_not_triggered"].format(coin.title(), current, direction, target),
            parse_mode="Markdown",
        )


def get_handlers():
    return [
        CommandHandler("price", price),
        CommandHandler("alert", alert),
    ]
