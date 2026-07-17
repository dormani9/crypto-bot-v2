from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from ..utils import fetch_prices


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            "Usage: `/price btc eth sol`\n"
            "Example: `/price bitcoin ethereum solana`",
            parse_mode="Markdown",
        )
        return

    try:
        data = fetch_prices(args)
    except Exception:
        await update.message.reply_text("Error fetching prices.")
        return

    if not data:
        await update.message.reply_text("No data found.")
        return

    lines = ["💰 *Live Prices*\n"]
    for coin_id, info in data.items():
        price_usd = info.get("usd", 0)
        change = info.get("usd_24h_change")
        change_str = f"{change:+.2f}%" if change else "N/A"
        icon = "🟢" if change and change >= 0 else "🔴"
        lines.append(
            f"{icon} *{coin_id.title()}*: `${price_usd:,.2f}` _{change-str}_"
        )

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def alert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3:
        await update.message.reply_text(
            "Usage: `/alert btc above 70000`\n"
            "Example: `/alert bitcoin above 70000`",
            parse_mode="Markdown",
        )
        return

    coin, direction, target_str = args[0].lower(), args[1].lower(), args[2]
    if direction not in ("above", "below"):
        await update.message.reply_text("Use `above` or `below`.", parse_mode="Markdown")
        return

    try:
        target = float(target_str)
    except ValueError:
        await update.message.reply_text("Invalid price.")
        return

    try:
        data = fetch_prices([coin])
    except Exception:
        await update.message.reply_text("Error fetching price.")
        return

    if coin not in data:
        await update.message.reply_text(f"Coin `{coin}` not found.", parse_mode="Markdown")
        return

    current = data[coin]["usd"]
    triggered = (direction == "above" and current > target) or (
        direction == "below" and current < target
    )

    if triggered:
        await update.message.reply_text(
            f"⚠️ *Alert triggered!*\n{coin.title()} `${current:,.2f}` {direction} `${target:,.2f}`",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text(
            f"{coin.title()} is `${current:,.2f}`. Not {direction} `${target:,.2f}` yet.",
            parse_mode="Markdown",
        )


def get_handlers():
    return [
        CommandHandler("price", price, filters.TEXT),
        CommandHandler("alert", alert, filters.TEXT),
    ]
