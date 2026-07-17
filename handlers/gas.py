import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters


async def gas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("⛽ Fetching...")

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
            f"⛽ *Ethereum Gas Fees*\n\n"
            f"🐢 Safe: `{safe:.1f}` Gwei\n"
            f"🚶 Normal: `{normal:.1f}` Gwei\n"
            f"🚀 Fast: `{fast:.1f}` Gwei\n\n"
            f"ETH: `${eth_price}`",
            parse_mode="Markdown",
        )
    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def get_handlers():
    return [CommandHandler("gas", gas, filters.TEXT)]
