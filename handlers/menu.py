import os

import feedparser
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes, filters

from utils import fetch_prices

FEEDS = [
    ("CoinDesk", "https://www.coindesk.com/arc/outboundfeeds/rss/"),
    ("CoinTelegraph", "https://cointelegraph.com/rss"),
]


async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "menu_price":
        prices = fetch_prices(["bitcoin", "ethereum", "solana", "ripple", "cardano"])
        lines = ["💰 *Live Prices*\n"]
        for cid, info in prices.items():
            p = info.get("usd", 0)
            ch = info.get("usd_24h_change")
            cs = f"{ch:+.2f}%" if ch else "N/A"
            ic = "🟢" if ch and ch >= 0 else "🔴"
            lines.append(f"{ic} *{cid.title()}*: `${p:,.2f}` _{cs}_")
        lines.append("\nTry: `/price btc eth`")
        kb = [[InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_fng":
        res = requests.get("https://api.alternative.me/fng/", params={"limit": 7}, timeout=10)
        d = res.json()["data"]
        emojis = {"Extreme Fear": "😱", "Fear": "😨", "Neutral": "😐", "Greed": "😊", "Extreme Greed": "🤑"}
        em = emojis.get(d[0]["value_classification"], "🤔")
        lines = [f"{em} *Fear & Greed*\n**{d[0]['value']}/100** — {d[0]['value_classification']}\n", "📊 *7 days:*"]
        for e in d:
            lines.append(f"  {e['timestamp'][:10]} → {e['value']}")
        kb = [[InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_news":
        articles = []
        for src, url in FEEDS:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                articles.append({"title": entry.title, "url": entry.link, "source": src})
        lines = ["📰 *Latest News*\n"]
        for i, a in enumerate(articles[:5], 1):
            lines.append(f"{i}. [{a['title']}]({a['url']})\n   — {a['source']}")
        kb = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="menu_news")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_back")],
        ]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_whale":
        key = os.getenv("ETHERSCAN_API_KEY")
        if not key:
            kb = [[InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]
            await query.edit_message_text("Set `ETHERSCAN_API_KEY` in .env\nGet one: etherscan.io/myapikey", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
            return

        eth_r = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
        eth_p = eth_r.json().get("ethereum", {}).get("usd", 0)
        r = requests.get("https://api.etherscan.io/api", params={
            "module": "account", "action": "txlist",
            "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
            "startblock": 0, "endblock": 99999999, "sort": "desc", "apikey": key,
        }, timeout=10)
        txs = r.json().get("result", [])

        lines = ["🐋 *Whale Transactions*\n"]
        c = 0
        for tx in txs:
            if c >= 5: break
            v = int(tx["value"]) / 1e18
            if v * eth_p < 1_000_000: continue
            lines.append(f"🔹 *${v * eth_p:,.0f}* ({v:,.2f} ETH)\n   `{tx['from'][:6]}...{tx['from'][-4:]}` → `{tx['to'][:6]}...{tx['to'][-4:]}`")
            c += 1
        if c == 0: lines.append("None found.")
        kb = [[InlineKeyboardButton("🔄 Refresh", callback_data="menu_whale")], [InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_gas":
        er = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
        ep = er.json().get("ethereum", {}).get("usd", "?")
        gr = requests.get("https://ethgasstation.info/api/ethgasAPI.json", timeout=10)
        gd = gr.json()
        s, n, f = gd.get("safeLow", 10) / 10, gd.get("average", 20) / 10, gd.get("fast", 30) / 10
        text = f"⛽ *Gas Fees*\n\n🐢 Safe: `{s:.1f}` Gwei\n🚶 Normal: `{n:.1f}` Gwei\n🚀 Fast: `{f:.1f}` Gwei\n\nETH: `${ep}`"
        kb = [[InlineKeyboardButton("🔄 Refresh", callback_data="menu_gas")], [InlineKeyboardButton("🔙 Back", callback_data="menu_back")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_portfolio":
        await query.edit_message_text(
            "💼 *Portfolio*\n\n"
            "`/add bitcoin 0.5` — add coins\n"
            "`/remove bitcoin` — remove\n"
            "`/portfolio` — view all",
            parse_mode="Markdown",
        )

    elif data == "menu_ai":
        await query.edit_message_text(
            "🤖 *AI Assistant*\n\n"
            "Powered by Google Gemini (free).\n\n"
            "Usage: `/ask what is DeFi?`\n"
            "Example: `/ask explain blockchain`",
            parse_mode="Markdown",
        )

    elif data == "menu_back":
        keyboard = [
            [InlineKeyboardButton("💰 Price", callback_data="menu_price"), InlineKeyboardButton("😱 F&G", callback_data="menu_fng")],
            [InlineKeyboardButton("📰 News", callback_data="menu_news"), InlineKeyboardButton("🐋 Whale", callback_data="menu_whale")],
            [InlineKeyboardButton("⛽ Gas", callback_data="menu_gas"), InlineKeyboardButton("💼 Portfolio", callback_data="menu_portfolio")],
            [InlineKeyboardButton("🤖 AI", callback_data="menu_ai")],
        ]
        await query.edit_message_text(
            "🚀 *Crypto Bot v2*\n\nChoose a feature:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


def get_handlers():
    return [CallbackQueryHandler(menu_callback, pattern="^menu_")]
