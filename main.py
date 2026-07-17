import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from handlers import fng, gas, menu, news, portfolio, price, start, toman, whale

from lang import EN, FA, get_lang

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
load_dotenv()

logger = logging.getLogger(__name__)

FREEMODEL_KEY = os.getenv("FREEMODEL_API_KEY")
BASE_URLS = [
    "https://api.freemodel.dev/v1",
    "https://vip-sg.freemodel.dev/v1",
    "https://api-t2-sg.freemodel.dev/v1",
]

AI_SYSTEM = (
    "You are a cryptocurrency expert. Answer concisely and accurately "
    "about crypto, blockchain, DeFi, trading, and market analysis."
)


async def _ai_call(question: str, client: OpenAI) -> str:
    res = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": AI_SYSTEM},
            {"role": "user", "content": question},
        ],
        max_tokens=500,
        timeout=15,
    )
    return res.choices[0].message.content


async def ai_fallback(update: Update, context):
    if not FREEMODEL_KEY:
        return

    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN
    question = update.message.text.strip()

    msg = await update.message.reply_text(t["ai_thinking"])

    for url in BASE_URLS:
        try:
            client = OpenAI(api_key=FREEMODEL_KEY, base_url=url)
            answer = await _ai_call(question, client)
            await msg.edit_text(f"🤖 *AI Assistant*\n\n{answer}", parse_mode="Markdown")
            return
        except Exception:
            logger.warning(f"AI fallback failed on {url}, trying next...")
            continue

    await msg.edit_text(f"{t['ai_error']} All AI endpoints failed.")


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_token_here":
        print("ERROR: Set TELEGRAM_BOT_TOKEN in .env")
        sys.exit(1)

    app = ApplicationBuilder().token(token).build()

    for module in [price, fng, news, whale, gas, portfolio, toman, menu]:
        for handler in module.get_handlers():
            app.add_handler(handler)

    for handler in start.get_handlers():
        app.add_handler(handler)
    for handler in start.get_callback_handlers():
        app.add_handler(handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_fallback))

    print("Bot v2 is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
