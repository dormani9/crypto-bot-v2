import os

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_URL = "https://api.etherscan.io/api"
WHALE_THRESHOLD = 1_000_000


async def whale(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not ETHERSCAN_KEY:
        await update.message.reply_text(t["whale_error"], parse_mode="Markdown")
        return

    msg = await update.message.reply_text(t["whale_scanning"])

    try:
        eth_resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
            timeout=10,
        )
        eth_price = eth_resp.json().get("ethereum", {}).get("usd", 0)

        params = {
            "module": "account",
            "action": "txlist",
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "apikey": ETHERSCAN_KEY,
        }
        res = requests.get(ETHERSCAN_URL, params=params, timeout=10)
        res.raise_for_status()
        result = res.json().get("result", [])
    except Exception as e:
        await msg.edit_text(f"{t['ai_error']} {e}")
        return

    lines = [t["whale_title"]]
    count = 0
    for tx in result:
        if count >= 5:
            break
        value_eth = int(tx["value"]) / 1e18
        if value_eth * eth_price < WHALE_THRESHOLD:
            continue
        lines.append(
            f"🔹 *${value_eth * eth_price:,.0f}* ({value_eth:,.2f} ETH)\n"
            f"   From `{tx['from'][:6]}...{tx['from'][-4:]}`\n"
            f"   To `{tx['to'][:6]}...{tx['to'][-4:] if tx['to'] else 'N/A'}`\n"
            f"   [`{tx['hash'][:10]}...{tx['hash'][-6:]}`](https://etherscan.io/tx/{tx['hash']})\n"
        )
        count += 1

    if count == 0:
        lines.append(t["whale_none"])

    await msg.edit_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


def get_handlers():
    return [CommandHandler("whale", whale, filters.TEXT)]
