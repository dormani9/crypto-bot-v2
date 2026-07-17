import feedparser
import logging
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

logger = logging.getLogger(__name__)

EN_FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]

_cache = {"en": [], "fa": []}

def refresh_cache():
    articles = []
    for source, url in EN_FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                articles.append({"title": entry.title, "url": entry.link, "source": source})
        except Exception as e:
            logger.warning(f"news refresh {source}: {e}")
    _cache["en"] = articles[:10]
    _cache["fa"] = []
    logger.info(f"news cache refreshed: {len(_cache['en'])} articles")


async def _translate_titles(articles):
    import os
    from openai import OpenAI
    key = os.getenv("FREEMODEL_API_KEY")
    if not key:
        return articles
    titles = "\n".join(a["title"] for a in articles)
    try:
        client = OpenAI(api_key=key, base_url="https://api.freemodel.dev/v1")
        res = client.chat.completions.create(
            model="gpt-5.4-mini",
            messages=[{"role": "user", "content": f"Translate these crypto news headlines to Persian. Return one per line, no numbers or dashes:\n{titles}"}],
            max_tokens=500,
            timeout=15,
        )
        translated = [l.strip() for l in res.choices[0].message.content.strip().split("\n") if l.strip()]
        out = []
        for i, a in enumerate(articles):
            t = translated[i] if i < len(translated) else a["title"]
            out.append({"title": t, "url": a["url"], "source": a["source"]})
        return out
    except Exception as e:
        logger.warning(f"news translate: {e}")
        return articles


def get_cached(lang="en"):
    if lang == "fa" and not _cache["fa"]:
        return None
    return _cache.get(lang, _cache["en"])


def set_fa_cache(articles):
    _cache["fa"] = articles


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    articles = _cache["en"] or []
    if not articles:
        await update.message.reply_text("No news found.")
        return
    lines = ["📰 *Latest Crypto News*\n"]
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. [{a['title']}]({a['url']})\n   — {a['source']}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True)


def get_handlers():
    return [CommandHandler("news", news)]
