from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang
from utils import fetch_toman_price


async def toman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    msg = await update.message.reply_text(
        "💱 در حال دریافت قیمت‌ها..." if t == FA else "💱 Fetching prices..."
    )

    usdt_toman, dollar_toman, source = fetch_toman_price()

    if not usdt_toman:
        await msg.edit_text(
            "❌ خطا در دریافت قیمت از تمام منابع.\n"
            "احتمالاً سرورهای ایران از Railway قابل دسترسی نیستند."
            if t == FA else
            "❌ All sources failed.\n"
            "Iranian servers may not be reachable from Railway."
        )
        return

    lines = [
        "💱 *قیمت‌های لحظه‌ای بازار ایران*" if t == FA else "💱 *Iran Market Rates*\n",
        "",
        f"💵 *1 USDT* = `{usdt_toman:,}` تومان" if t == FA else f"💵 *1 USDT* = `{usdt_toman:,}` Toman",
        f"🇺🇸 *1 USD* ≈ `{dollar_toman:,}` تومان" if t == FA else f"🇺🇸 *1 USD* ≈ `{dollar_toman:,}` Toman",
        "",
        f"📡 {source}",
    ]

    await msg.edit_text("\n".join(lines), parse_mode="Markdown")


def get_handlers():
    return [CommandHandler("toman", toman, filters.TEXT)]
