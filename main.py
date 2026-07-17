import logging
import os
import sys

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from handlers import ai, fng, gas, menu, news, portfolio, price, start, whale

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
load_dotenv()


def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "your_token_here":
        print("ERROR: Set TELEGRAM_BOT_TOKEN in .env")
        sys.exit(1)

    app = ApplicationBuilder().token(token).build()

    for module in [start, price, fng, news, whale, gas, portfolio, ai, menu]:
        for handler in module.get_handlers():
            app.add_handler(handler)

    print("Bot v2 is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
