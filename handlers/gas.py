import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang


async def gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    msg = await update.message.reply_text(t["gas_fetching"])

    try:
        eth_resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
            timeout=10,
        )
        eth_price = eth_resp.json().get("ethereum", {}).get("usd", "?")

        gas_resp = requests.get("https://ethgasstation.info/api/ethgasAPI.json", timeout=10)
        gas_resp.raise_for_status()
        data = gas_resp.json()
        safe = data.get("safeLow", 10) / 10
        normal = data.get("average", 20) / 10
        fast = data.get("fast", 30) / 10

        await msg.edit_text(
            f"{t['gas_title']}"
            f"{t['gas_safe']} `{safe:.1f}` Gwei\n"
            f"{t['gas_normal']} `{normal:.1f}` Gwei\n"
            f"{t['gas_fast']} `{fast:.1f}` Gwei\n\n"
            f"ETH: `${eth_price}`",
            parse_mode="Markdown",
        )
    except Exception as e:
        await msg.edit_text(f"{t['ai_error']} {e}")


def get_handlers():
    return [CommandHandler("gas", gas, filters.TEXT)]
