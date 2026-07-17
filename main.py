import logging
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from handlers import fng, gas, menu, news, price, start, toman, watch, whale

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


async def _send_wallet_notification(uid: int, tx: dict, context):
    lang_code = get_lang(uid)
    from_short = tx["from"][:10] + "..." + tx["from"][-6:] if tx.get("from") and len(tx["from"]) > 16 else tx.get("from", "?")
    to_short = tx["to"][:10] + "..." + tx["to"][-6:] if tx.get("to") and len(tx["to"]) > 16 else tx.get("to", "N/A")
    tx_hash = tx.get("hash", "?")
    tx_short = tx_hash[:10] + "..." + tx_hash[-6:] if len(tx_hash) > 16 else tx_hash
    chain_tag = f" [{tx['chain']}]"
    header = "🔔 *Token Tx*" + chain_tag if tx["is_token"] else "🔔 *New Tx*" + chain_tag
    text = (
        f"{header}\n\n"
        f"💱 {tx['label']}\n"
        f"📤 {from_short}\n"
        f"📥 {to_short}\n"
        f"📋 `{tx_short}`\n"
        f"🔗 [{'مشاهده' if lang_code == 'fa' else 'View'}](https://etherscan.io/tx/{tx_hash})"
    )
    try:
        await context.bot.send_message(chat_id=uid, text=text, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception as e:
        logger.warning(f"Failed to send wallet notification to {uid}: {e}")


async def check_wallets(context: ContextTypes.DEFAULT_TYPE):
    notifications = watch.check_new_txs()
    for uid_str, txs in notifications.items():
        for tx in txs:
            await _send_wallet_notification(int(uid_str), tx, context)


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

    async def post_init(app):
        await app.bot.set_my_commands([
            ("start", "Start / راه‌اندازی"),
            ("help", "Help / راهنما"),
            ("price", "Crypto prices / قیمت"),
            ("fng", "Fear & Greed"),
            ("news", "Crypto news / اخبار"),
            ("whale", "Whale alerts"),
            ("gas", "Gas fees"),
            ("ask", "Ask AI / بپرس"),
            ("toman", "USD to Toman"),
            ("watch", "Monitor wallet / رصد ولت"),
            ("unwatch", "Stop monitoring"),
            ("wallets", "List watched wallets"),
            ("check", "Scan wallets now"),
        ])
        news.refresh_cache()

    app = ApplicationBuilder().token(token).post_init(post_init).build()

    for module in [price, fng, news, whale, gas, toman, menu, watch]:
        for handler in module.get_handlers():
            app.add_handler(handler)

    for handler in start.get_handlers():
        app.add_handler(handler)
    for handler in start.get_callback_handlers():
        app.add_handler(handler)

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_fallback))

    jq = app.job_queue
    if jq:
        jq.run_repeating(check_wallets, interval=15, first=10)
        jq.run_repeating(lambda _: news.refresh_cache(), interval=3600, first=60)

    print("Bot v2 is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
