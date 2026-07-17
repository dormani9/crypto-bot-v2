import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

FNG_URL = "https://api.alternative.me/fng/"


async def fng(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("Loading...")

    try:
        res = requests.get(FNG_URL, params={"limit": 7}, timeout=10)
        res.raise_for_status()
        data = res.json()["data"]
    except Exception:
        await msg.edit_text("Error fetching Fear & Greed Index.")
        return

    latest = data[0]
    emojis = {"Extreme Fear": "😱", "Fear": "😨", "Neutral": "😐", "Greed": "😊", "Extreme Greed": "🤑"}
    emoji = emojis.get(latest["value_classification"], "🤔")

    lines = [
        f"{emoji} *Fear & Greed Index*",
        f"**{latest['value']}/100** — {latest['value_classification']}\n",
        "📊 *Last 7 days:*",
    ]
    for entry in data:
        lines.append(f"  {entry['timestamp'][:10]} → {entry['value']} {entry['value_classification']}")

    await msg.edit_text("\n".join(lines), parse_mode="Markdown")


def get_handlers():
    return [CommandHandler("fng", fng, filters.TEXT)]
