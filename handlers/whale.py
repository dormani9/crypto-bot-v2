import os

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang

ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_V2 = "https://api.etherscan.io/v2/api"
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
            "chainid": 1,
            "module": "account",
            "action": "txlist",
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
            "startblock": 0,
            "endblock": 99999999,
            "sort": "desc",
            "page": 1,
            "offset": 10,
            "apikey": ETHERSCAN_KEY,
        }
        res = requests.get(ETHERSCAN_V2, params=params, timeout=15)
        res.raise_for_status()
        result = res.json().get("result", [])
        if not isinstance(result, list):
            result = []
    except Exception as e:
        await msg.edit_text(f"{t['ai_error']} {e}")
        return

    lines = [t["whale_title"]]
    count = 0
    for tx in result:
        if count >= 5:
            break
        try:
            value_eth = int(tx.get("value", 0)) / 1e18
        except (ValueError, TypeError):
            continue
        if value_eth * eth_price < WHALE_THRESHOLD:
            continue
        from_addr = tx.get("from", "?")[:6] + "..." + tx.get("from", "?")[-4:]
        to_addr = tx.get("to", "")[:6] + "..." + tx.get("to", "")[-4:] if tx.get("to") else "N/A"
        tx_hash = tx.get("hash", "?")
        tx_short = tx_hash[:10] + "..." + tx_hash[-6:] if len(tx_hash) > 16 else tx_hash
        lines.append(
            f"🔹 *${value_eth * eth_price:,.0f}* ({value_eth:,.2f} ETH)\n"
            f"   From `{from_addr}`\n"
            f"   To `{to_addr}`\n"
            f"   [`{tx_short}`](https://etherscan.io/tx/{tx_hash})\n"
        )
        count += 1

    if count == 0:
        lines.append(t["whale_none"])

    await msg.edit_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


def get_handlers():
    return [CommandHandler("whale", whale, filters.TEXT)]
