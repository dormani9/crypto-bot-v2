import os

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_V2 = "https://api.etherscan.io/v2/api"


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

        safe = normal = fast = "?"

        if ETHERSCAN_KEY:
            params = {
                "chainid": 1,
                "module": "gastracker",
                "action": "gasoracle",
                "apikey": ETHERSCAN_KEY,
            }
            gas_resp = requests.get(ETHERSCAN_V2, params=params, timeout=10)
            data = gas_resp.json().get("result")
            if isinstance(data, dict):
                safe = data.get("SafeGasPrice", "?")
                normal = data.get("ProposeGasPrice", "?")
                fast = data.get("FastGasPrice", "?")

        text = (
            f"{t['gas_title']}"
            f"{t['gas_safe']} `{safe}` Gwei\n"
            f"{t['gas_normal']} `{normal}` Gwei\n"
            f"{t['gas_fast']} `{fast}` Gwei\n\n"
            f"ETH: `${eth_price}`"
        )
        if not ETHERSCAN_KEY:
            text += "\n\n⚠️ Set ETHERSCAN_API_KEY for live gas"

        await msg.edit_text(text, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"{t['ai_error']} {e}")


def get_handlers():
    return [CommandHandler("gas", gas, filters.TEXT)]
