import feedparser
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]
TRANSLATOR = GoogleTranslator(source="en", target="fa")


def _fetch(limit: int):
    articles = []
    for source, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:limit]:
                articles.append({"title": entry.title, "url": entry.link, "source": source})
        except Exception:
            continue
    return articles[:limit]


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = min(int(context.args[0]), 10) if context.args and context.args[0].isdigit() else 5
    articles = _fetch(limit)

    if not articles:
        await update.message.reply_text("No news found.")
        return

    lines = ["📰 *Latest Crypto News*\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['title']}]({a['url']})\n   — {a['source']}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


async def fnews(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = min(int(context.args[0]), 10) if context.args and context.args[0].isdigit() else 5
    articles = _fetch(limit)

    if not articles:
        await update.message.reply_text("خبری یافت نشد.")
        return

    lines = ["📰 *آخرین اخبار کریپتو*\n"]
    for i, a in enumerate(articles, 1):
        try:
            title_fa = TRANSLATOR.translate(a["title"])
        except Exception:
            title_fa = a["title"]
        lines.append(f"🔹 *{title_fa}*")
        lines.append(f"   📎 [مشاهده مطلب]({a['url']}) — {a['source']}\n")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


def get_handlers():
    return [
        CommandHandler("news", news),
        CommandHandler("fnews", fnews),
    ]
