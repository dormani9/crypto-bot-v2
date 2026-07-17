import logging
import os
import sys
import time

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from handlers import fng, gas, menu, news, portfolio, price, start, toman, watch, whale

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


async def check_wallets(context: ContextTypes.DEFAULT_TYPE):
    notifications = watch.check_new_txs()
    for uid_str, txs in notifications.items():
        for tx in txs:
            uid = int(uid_str)
            lang_code = get_lang(uid)
            t = FA if lang_code == "fa" else EN
            addr = tx["_address"]
            value_eth = int(tx.get("value", 0)) / 1e18
            from_addr = tx.get("from", "?")[:10] + "..." + tx.get("from", "?")[-6:]
            to_addr = tx.get("to", "")[:10] + "..." + tx.get("to", "")[-6:] if tx.get("to") else "N/A"
            tx_hash = tx.get("hash", "?")
            usd_value = value_eth * _get_eth_price()
            text = t["watch_notification"].format(
                tx_hash[:10] + "..." + tx_hash[-6:] if len(tx_hash) > 16 else tx_hash,
                f"{value_eth:.4f}",
                usd_value,
                from_addr,
                to_addr,
                tx_hash,
            )
            try:
                await context.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown", disable_web_page_preview=True)
            except Exception as e:
                logger.warning(f"Failed to send wallet notification to {uid}: {e}")


_eth_price_cache = 0.0
_eth_price_ts = 0.0


def _get_eth_price() -> float:
    global _eth_price_cache, _eth_price_ts
    now = time.time()
    if now - _eth_price_ts > 30:
        try:
            import requests
            r = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=5)
            _eth_price_cache = r.json().get("ethereum", {}).get("usd", 0)
            _eth_price_ts = now
        except Exception:
            pass
    return _eth_price_cache


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

    for module in [price, fng, news, whale, gas, portfolio, toman, menu, watch]:
        for handler in module.get_handlers():
            app.add_handler(handler)

    for handler in start.get_handlers():
        app.add_handler(handler)
    for handler in start.get_callback_handlers():
        app.add_handler(handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_fallback))

    job_queue = app.job_queue
    if job_queue:
        job_queue.run_repeating(check_wallets, interval=45, first=10)

    print("Bot v2 is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
