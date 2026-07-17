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

FREEMODEL_KEY = os.getenv("FREEMODEL_API_KEY")
BASE_URL = "https://api.freemodel.dev/v1"
AI_CLIENT = OpenAI(api_key=FREEMODEL_KEY, base_url=BASE_URL) if FREEMODEL_KEY else None

AI_SYSTEM = (
    "You are a cryptocurrency expert. Answer concisely and accurately "
    "about crypto, blockchain, DeFi, trading, and market analysis."
)


async def ai_fallback(update: Update, context):
    if not AI_CLIENT:
        return

    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN
    question = update.message.text.strip()

    msg = await update.message.reply_text(t["ai_thinking"])

    try:
        res = AI_CLIENT.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[
                {"role": "system", "content": AI_SYSTEM},
                {"role": "user", "content": question},
            ],
            max_tokens=500,
            timeout=30,
        )
        answer = res.choices[0].message.content
        await msg.edit_text(f"🤖 *AI Assistant*\n\n{answer}", parse_mode="Markdown")
    except Exception as e:
        await msg.edit_text(f"{t['ai_error']} {e}")


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
