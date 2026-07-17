from typing import Optional, Tuple

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang

SOURCES = [
    {
        "name": "Nobitex",
        "url": "https://api.nobitex.ir/market/stats",
        "params": {"srcCurrency": "usdt"},
        "parse": lambda d: int(d["stats"]["usdt"]["latest"]),
    },
    {
        "name": "Wallex",
        "url": "https://api.wallex.ir/v1/markets",
        "parse": lambda d: int(float([m for m in d["result"] if m["symbol"] == "USDTIRT"][0]["price"])),
    },
    {
        "name": "Bit24",
        "url": "https://api.bit24.ir/api/v1/markets",
        "parse": lambda d: int(float([m for m in d if m["symbol"] == "USDTIRT"][0]["stats"]["last"])),
    },
]


def fetch_price() -> Tuple[Optional[int], Optional[int], Optional[str]]:
    for src in SOURCES:
        try:
            params = src.get("params", {})
            res = requests.get(src["url"], params=params, timeout=8)
            res.raise_for_status()
            data = res.json()
            usdt_price = src["parse"](data)
            return usdt_price, usdt_price, src["name"]
        except Exception:
            continue
    return None, None, None


async def toman(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    msg = await update.message.reply_text(
        "💱 در حال دریافت قیمت‌ها..." if t == FA else "💱 Fetching prices..."
    )

    usdt_toman, dollar_toman, source = fetch_price()

    if not usdt_toman:
        await msg.edit_text("خطا در دریافت قیمت از تمام منابع." if t == FA else "All sources failed.")
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
