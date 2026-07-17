import logging
import os

from openai import OpenAI
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from lang import EN, FA, get_lang

API_KEY = os.getenv("FREEMODEL_API_KEY")
BASE_URLS = [
    "https://api.freemodel.dev/v1",
    "https://vip-sg.freemodel.dev/v1",
    "https://api-t2-sg.freemodel.dev/v1",
]

logger = logging.getLogger(__name__)

SYSTEM = (
    "You are a cryptocurrency expert. Answer concisely and accurately "
    "about crypto, blockchain, DeFi, trading, and market analysis."
)


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not API_KEY:
        await update.message.reply_text(t["ai_not_configured"], parse_mode="Markdown")
        return

    question = " ".join(context.args)
    if not question:
        await update.message.reply_text(t["ai_usage"], parse_mode="Markdown")
        return

    msg = await update.message.reply_text(t["ai_thinking"])

    for url in BASE_URLS:
        try:
            client = OpenAI(api_key=API_KEY, base_url=url)
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
            return
        except Exception:
            logger.warning(f"AI request failed on {url}, trying next...")
            continue

    await msg.edit_text(f"{t['ai_error']} All AI endpoints failed.")


def get_handlers():
    return [CommandHandler("ask", ask)]
