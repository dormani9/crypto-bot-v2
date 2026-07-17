import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang

FNG_URL = "https://api.alternative.me/fng/"


async def fng(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    msg = await update.message.reply_text(t["fng_title"])

    try:
        res = requests.get(FNG_URL, params={"limit": 7}, timeout=10)
        res.raise_for_status()
        data = res.json()["data"]
    except Exception:
        await msg.edit_text(t["fng_error"])
        return

    latest = data[0]
    emojis = {"Extreme Fear": "😱", "Fear": "😨", "Neutral": "😐", "Greed": "😊", "Extreme Greed": "🤑"}
    emoji = emojis.get(latest["value_classification"], "🤔")

    lines = [
        f"{emoji} *Fear & Greed Index*",
        f"**{latest['value']}/100** — {latest['value_classification']}\n",
        t["fng_7days"],
    ]
    for entry in data:
        lines.append(f"  {entry['timestamp'][:10]} → {entry['value']}")

    await msg.edit_text("\n".join(lines), parse_mode="Markdown")


def get_handlers():
    return [CommandHandler("fng", fng, filters.TEXT)]
