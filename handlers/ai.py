import os

from google import genai
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

SYSTEM = (
    "You are a cryptocurrency expert. Answer concisely and accurately "
    "about crypto, blockchain, DeFi, trading, and market analysis."
)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not client:
        await update.message.reply_text(
            "AI is not configured.\n"
            "Get a *free* Gemini API key:\n"
            "https://aistudio.google.com/apikey\n\n"
            "Then set `GEMINI_API_KEY` in .env",
            parse_mode="Markdown",
        )
        return

    question = " ".join(context.args)
    if not question:
        await update.message.reply_text("Usage: `/ask what is Ethereum?`", parse_mode="Markdown")
        return

    msg = await update.message.reply_text("🤔 Thinking...")

    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{SYSTEM}\n\nUser: {question}",
        )
        answer = res.text.strip()
        await msg.edit_text(f"🤖 *AI Assistant*\n\n{answer}", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"Error: {e}")


def get_handlers():
    return [CommandHandler("ask", ask, filters.TEXT)]
