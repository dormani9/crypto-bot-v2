import os

from openai import OpenAI
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

API_KEY = os.getenv("FREEMODEL_API_KEY")
BASE_URL = "https://api.freemodel.dev/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL) if API_KEY else None

SYSTEM = (
    "You are a cryptocurrency expert. Answer concisely and accurately "
    "about crypto, blockchain, DeFi, trading, and market analysis."
)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text(
            "AI is not configured.\n"
            "Set `FREEMODEL_API_KEY` in .env",
            parse_mode="Markdown",
        )
        return

    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("Usage: `/ask what is Ethereum?`", parse_mode="Markdown")
        return

    msg = await update.message.reply_text("🤔 Thinking...")

    try:
        res = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
            timeout=30,
        )
        answer = res.choices[0].message.content
        await msg.edit_text(f"🤖 *AI Assistant*\n\n{answer}", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def get_handlers():
    return [CommandHandler("ask", ask, filters.TEXT)]
