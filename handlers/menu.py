import os

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, ContextTypes, filters

from handlers import news as news_mod
from lang import EN, FA, get_lang
from utils import fetch_prices, fetch_toman_price


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
        kb = [[InlineKeyboardButton("🔄", callback_data="menu_price")],
              [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
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
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_fng")],
              [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_news":
        articles = news_mod.get_cached(lang)
        if articles is None and lang == "fa":
            en_articles = news_mod.get_cached("en") or []
            if en_articles:
                translated = await news_mod._translate_titles(en_articles)
                news_mod.set_fa_cache(translated)
                articles = translated
        if not articles:
            articles = news_mod.get_cached("en") or []
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
            r = requests.get("https://api.etherscan.io/v2/api", params={
                "chainid": 1, "module": "account", "action": "txlist",
                "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                "startblock": 0, "endblock": 99999999, "sort": "desc",
                "page": 1, "offset": 10, "apikey": key,
            }, timeout=10)
            result = r.json().get("result", [])
            txs = result if isinstance(result, list) else []
        except Exception as e:
            await query.edit_message_text(f"{t['ai_error']} {e}")
            return

        lines = [t["whale_title"]]
        c = 0
        for tx in txs:
            if c >= 5: break
            try:
                v = int(tx.get("value", 0)) / 1e18
                if v * eth_p < 1_000_000: continue
                lines.append(f"🔹 *${v * eth_p:,.0f}* ({v:,.2f} ETH)\n   `{tx['from'][:6]}...{tx['from'][-4:]}` → `{tx['to'][:6]}...{tx['to'][-4:]}`")
                c += 1
            except Exception:
                continue
        if c == 0: lines.append(t["whale_none"])
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_whale")], [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_gas":
        try:
            er = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
            ep = er.json().get("ethereum", {}).get("usd", "?")
            gk = os.getenv("ETHERSCAN_API_KEY")
            s = n = f = "?"
            if gk:
                gr = requests.get("https://api.etherscan.io/v2/api", params={"chainid": 1, "module": "gastracker", "action": "gasoracle", "apikey": gk}, timeout=10)
                gd = gr.json().get("result")
                if isinstance(gd, dict):
                    s, n, f = gd.get("SafeGasPrice", "?"), gd.get("ProposeGasPrice", "?"), gd.get("FastGasPrice", "?")
            text = f"{t['gas_title']}{t['gas_safe']} `{s}` Gwei\n{t['gas_normal']} `{n}` Gwei\n{t['gas_fast']} `{f}` Gwei\n\nETH: `${ep}`"
        except Exception as e:
            text = f"{t['ai_error']} {e}"
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_gas")], [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text(text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_wallet":
        text = t["wallet_title"] + t["wallet_add"] + t["wallet_remove"] + t["wallet_list"] + t["wallet_check"]
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "menu_ai":
        text = t["ai_title"] + t["ai_desc"] + t["ai_usage"]
        await query.edit_message_text(text, parse_mode="Markdown")

    elif data == "menu_toman":
        usdt_t, dollar_t, src = fetch_toman_price()
        if usdt_t:
            lines = [
                f"💱 *{'قیمت‌های لحظه‌ای بازار ایران' if lang == 'fa' else 'Iran Market Rates'}*\n",
                f"💵 *1 USDT* = `{usdt_t:,}` {'تومان' if lang == 'fa' else 'Toman'}",
                f"🇺🇸 *1 USD* ≈ `{dollar_t:,}` {'تومان' if lang == 'fa' else 'Toman'}",
                f"📡 {src}",
            ]
        else:
            lines = [f"❌ {'خطا در دریافت قیمت' if lang == 'fa' else 'Error fetching prices'}."]
        kb = [[InlineKeyboardButton(t["refresh"], callback_data="menu_toman")],
              [InlineKeyboardButton(t["back"], callback_data="menu_back")]]
        await query.edit_message_text("\n".join(lines), parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_back":
        keyboard = [
            [InlineKeyboardButton(t["price"], callback_data="menu_price"), InlineKeyboardButton(t["fng"], callback_data="menu_fng")],
            [InlineKeyboardButton("💱 USD", callback_data="menu_toman"), InlineKeyboardButton(t["news"], callback_data="menu_news")],
            [InlineKeyboardButton(t["whale"], callback_data="menu_whale"), InlineKeyboardButton(t["gas"], callback_data="menu_gas")],
            [InlineKeyboardButton(t["wallet"], callback_data="menu_wallet"), InlineKeyboardButton(t["ai"], callback_data="menu_ai")],
        ]
        await query.edit_message_text(t["menu_title"], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


def get_handlers():
    return [CallbackQueryHandler(menu_callback, pattern="^menu_")]
