import os

import feedparser
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes, filters

from lang import EN, FA, get_lang
from utils import fetch_prices

FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    lang = get_lang(uid)
    t = FA if lang == "fa" else EN

    data = query.data

    if data == "menu_price":
        prices = fetch_prices(["bitcoin", "ethereum", "solana", "ripple", "cardano"])
        lines = [t["live_prices"]]
        for cid, info in prices.items():
            p = info.get("usd", 0)
            ch = info.get("usd_24h_change")
            cs = f"{ch:+.2f}%" if ch else "N/A"
            ic = "🟢" if ch and ch >= 0 else "🔴"
            lines.append(f"{ic} *{cid.title()}*: `${p:,.2f}` _{cs}_")
        lines.append(t["custom_coins"])
        kb = [[InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_fng":
        try:
            res = requests.get("https://api.alternative.me/fng/", params={"limit": 7}, timeout=10)
            d = res.json()["data"]
        except Exception:
            await query.edit_message_text(t["fng_error"])
            return
        emojis = {"Extreme Fear": "😱", "Fear": "😨", "Neutral": "😐", "Greed": "😊", "Extreme Greed": "🤑"}
        em = emojis.get(d[0]["value_classification"], "🤔")
        lines = [f"{em} *Fear & Greed*\n**{d[0]['value']}/100** — {d[0]['value_classification']}\n", t["fng_7days"]]
        for e in d:
            lines.append(f"  {e['timestamp'][:10]} → {e['value']}")
        kb = [[InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_news":
        articles = []
        for src, url in FEEDS:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                articles.append({"title": entry.title, "url": entry.link, "source": src})
        lines = [t["news_title"]]
        for i, a in enumerate(articles[:5], 1):
            lines.append(f"{i}. [{a['title']}]({a['url']})\n   — {a['source']}")
        kb = [
            [InlineKeyboardButton(t["refresh"], callback_data="menu_news")],
            [InlineKeyboardButton(t["back"], callback_data="menu_back")],
        ]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_whale":
        key = os.getenv("ETHERSCAN_API_KEY")
        if not key:
            kb = [[InlineKeyboardButton(t["back"], callback_data="menu_back")]]
            await query.edit_message_text(t["whale_error"], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
            return

        try:
            eth_r = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
            eth_p = eth_r.json().get("ethereum", {}).get("usd", 0)
            r = requests.get("https://api.etherscan.io/api", params={
                "module": "account", "action": "txlist",
                "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                "startblock": 0, "endblock": 99999999, "sort": "desc", "apikey": key,
            }, timeout=10)
            txs = r.json().get("result", [])
        except Exception as e:
            await query.edit_message_text(f"{t['ai_error']} {e}")
            return

        lines = [t["whale_title"]]
        c = 0
        for tx in txs:
            if c >= 5: break
            v = int(tx["value"]) / 1e18
            if v * eth_p < 1_000_000: continue
            lines.append(f"🔹 *${v * eth_p:,.0f}* ({v:,.2f} ETH)\n   `{tx['from'][:6]}...{tx['from'][-4:]}` → `{tx['to'][:6]}...{tx['to'][-4:]}`")
            c += 1
        if c == 0: lines.append(t["whale_none"])
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_whale")], [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_gas":
        try:
            er = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
            ep = er.json().get("ethereum", {}).get("usd", "?")
            gr = requests.get("https://ethgasstation.info/api/ethgasAPI.json", timeout=10)
            gd = gr.json()
            s, n, f = gd.get("safeLow", 10) / 10, gd.get("average", 20) / 10, gd.get("fast", 30) / 10
            text = f"{t['gas_title']}{t['gas_safe']} `{s:.1f}` Gwei\n{t['gas_normal']} `{n:.1f}` Gwei\n{t['gas_fast']} `{f:.1f}` Gwei\n\nETH: `${ep}`"
        except Exception as e:
            text = f"{t['ai_error']} {e}"
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_gas")], [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_portfolio":
        text = t["portfolio_title"] + t["portfolio_add"] + t["portfolio_remove"] + t["portfolio_view"]
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "menu_ai":
        text = t["ai_title"] + t["ai_desc"] + t["ai_usage"]
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "menu_back":
        keyboard = [
            [InlineKeyboardButton(t["price"], callback_data="menu_price"), InlineKeyboardButton(t["fng"], callback_data="menu_fng")],
            [InlineKeyboardButton(t["news"], callback_data="menu_news"), InlineKeyboardButton(t["whale"], callback_data="menu_whale")],
            [InlineKeyboardButton(t["gas"], callback_data="menu_gas"), InlineKeyboardButton(t["portfolio"], callback_data="menu_portfolio")],
            [InlineKeyboardButton(t["ai"], callback_data="menu_ai")],
        ]
        await query.edit_message_text(t["menu_title"], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


def get_handlers():
    return [CallbackQueryHandler(menu_callback, pattern="^menu_")]
