import json
import os
from pathlib import Path

DATA_FILE = Path(__file__).parent / "user_langs.json"


def _load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def _save(data):
    DATA_FILE.write_text(json.dumps(data))


def get_lang(user_id: int) -> str:
    return _load().get(str(user_id), "en")


def set_lang(user_id: int, lang: str):
    data = _load()
    data[str(user_id)] = lang
    _save(data)


FA = {
    "menu_title": "🚀 *ربات ارز دیجیتال v2*\n\nیک همراه همه‌کاره برای ارزهای دیجیتال.\nاز منوی زیر استفاده کن یا /help را بزن.\n\n✨ *جدید:* دستیار هوش مصنوعی رایگان!",
    "price": "💰 قیمت",
    "fng": "😱 ترس و طمع",
    "news": "📰 اخبار",
    "whale": "🐋 نهنگ‌ها",
    "gas": "⛽ کارمزد",
    "portfolio": "💼 پورتفولیو",
    "ai": "🤖 هوش مصنوعی",
    "back": "🔙 برگشت",
    "refresh": "🔄 تازه کردن",
    "help_title": "📚 *دستورات*\n\n",
    "help_price": "`/price btc eth` — قیمت لحظه‌ای\n",
    "help_alert": "`/alert btc above 70000` — هشدار قیمت\n",
    "help_fng": "`/fng` — شاخص ترس و طمع\n",
    "help_news": "`/news 5` — اخبار انگلیسی\n",
    "help_fnews": "`/fnews 5` — اخبار فارسی\n",
    "help_whale": "`/whale` — تراکنش‌های بزرگ\n",
    "help_gas": "`/gas` — کارمزد اتریوم\n",
    "help_portfolio": "`/add btc 0.5` / `/portfolio` — مدیریت سبد\n",
    "help_ask": "`/ask what is eth` — دستیار هوش مصنوعی\n",
    "live_prices": "💰 *قیمت‌های لحظه‌ای*\n",
    "custom_coins": "\nمثال: `/price btc eth`",
    "fng_title": "😱 *شاخص ترس و طمع*\n",
    "fng_7days": "📊 *۷ روز اخیر:*",
    "news_title": "📰 *آخرین اخبار*\n",
    "whale_title": "🐋 *تراکنش‌های نهنگ‌ها*\n",
    "whale_none": "تراکنش بزرگی یافت نشد.",
    "whale_error": "کلید Etherscan تنظیم نشده.\nدریافت کلید: etherscan.io/myapikey",
    "gas_title": "⛽ *کارمزد اتریوم*\n\n",
    "gas_safe": "🐢 کند:",
    "gas_normal": "🚶 معمولی:",
    "gas_fast": "🚀 سریع:",
    "portfolio_title": "💼 *مدیریت سبد*\n\n",
    "portfolio_add": "`/add bitcoin 0.5` — افزودن سکه\n",
    "portfolio_remove": "`/remove bitcoin` — حذف\n",
    "portfolio_view": "`/portfolio` — مشاهده همه\n",
    "portfolio_empty": "سبد خالی است.\nافزودن: `/add bitcoin 0.5`\nحذف: `/remove bitcoin`",
    "portfolio_total": "💰 *مجموع:",
    "ai_title": "🤖 *دستیار هوش مصنوعی*\n\n",
    "ai_desc": "قدرت گرفته از FreeModel.dev (رایگان).\n\n",
    "ai_usage": "روش استفاده: `/ask what is DeFi?`\nمثال: `/ask اتریوم چیست؟`",
    "ai_not_configured": "هوش مصنوعی تنظیم نشده.\n`FREEMODEL_API_KEY` را در .env تنظیم کن",
    "ai_thinking": "🤔 در حال فکر کردن...",
    "ai_error": "خطا:",
    "price_usage": "روش استفاده: `/price btc eth sol`\nمثال: `/price bitcoin ethereum solana`",
    "price_error": "خطا در دریافت قیمت‌ها.",
    "price_none": "اطلاعاتی یافت نشد.",
    "alert_usage": "روش استفاده: `/alert btc above 70000`\nمثال: `/alert bitcoin above 70000`",
    "alert_direction": "از `above` یا `below` استفاده کن.",
    "alert_invalid": "قیمت نامعتبر.",
    "alert_error": "خطا در دریافت قیمت.",
    "alert_not_found": "سکه `{}` یافت نشد.",
    "alert_triggered": "⚠️ *هشدار فعال شد!*\n{} ${:,.2f} {} ${:,.2f}",
    "alert_not_triggered": "{} ${:,.2f} است. هنوز {} ${:,.2f} نشده.",
    "fng_error": "خطا در دریافت شاخص ترس و طمع.",
    "news_none": "خبری یافت نشد.",
    "portfolio_added": "✅ {} {} به سبد اضافه شد.",
    "portfolio_removed": "✅ {} از سبد حذف شد.",
    "portfolio_not_found": "{} در سبد وجود ندارد.",
    "add_usage": "روش استفاده: `/add bitcoin 0.5`",
    "remove_usage": "روش استفاده: `/remove bitcoin`",
    "add_invalid": "مقدار نامعتبر.",
    "whale_scanning": "🐋 در حال جستجو...",
    "gas_fetching": "⛽ در حال دریافت...",
    "lang_set": "🌐 زبان به فارسی تغییر کرد.",
    "lang_en": "🌐 Language set to English.",
}

EN = {
    "menu_title": "🚀 *Crypto Bot v2*\n\nYour all-in-one cryptocurrency companion.\nUse the menu below or type /help.\n\n✨ *New:* Free AI assistant!",
    "price": "💰 Price",
    "fng": "😱 F&G Index",
    "news": "📰 News",
    "whale": "🐋 Whale Alert",
    "gas": "⛽ Gas Fee",
    "portfolio": "💼 Portfolio",
    "ai": "🤖 AI Assistant",
    "back": "🔙 Back",
    "refresh": "🔄 Refresh",
    "help_title": "📚 *Commands*\n\n",
    "help_price": "`/price btc eth` — current prices\n",
    "help_alert": "`/alert btc above 70000` — price check\n",
    "help_fng": "`/fng` — Fear & Greed Index\n",
    "help_news": "`/news 5` — English news\n",
    "help_fnews": "`/fnews 5` — اخبار فارسی\n",
    "help_whale": "`/whale` — large transactions\n",
    "help_gas": "`/gas` — Ethereum gas fees\n",
    "help_portfolio": "`/add btc 0.5` / `/portfolio` — track holdings\n",
    "help_ask": "`/ask what is eth` — AI assistant\n",
    "live_prices": "💰 *Live Prices*\n",
    "custom_coins": "\nTry: `/price btc eth`",
    "fng_title": "😱 *Fear & Greed Index*\n",
    "fng_7days": "📊 *Last 7 days:*",
    "news_title": "📰 *Latest News*\n",
    "whale_title": "🐋 *Whale Transactions*\n",
    "whale_none": "No large transactions found.",
    "whale_error": "Set `ETHERSCAN_API_KEY` in .env\nGet one: etherscan.io/myapikey",
    "gas_title": "⛽ *Ethereum Gas Fees*\n\n",
    "gas_safe": "🐢 Safe:",
    "gas_normal": "🚶 Normal:",
    "gas_fast": "🚀 Fast:",
    "portfolio_title": "💼 *Portfolio*\n\n",
    "portfolio_add": "`/add bitcoin 0.5` — add coins\n",
    "portfolio_remove": "`/remove bitcoin` — remove\n",
    "portfolio_view": "`/portfolio` — view all\n",
    "portfolio_empty": "Portfolio is empty.\nAdd: `/add bitcoin 0.5`\nRemove: `/remove bitcoin`",
    "portfolio_total": "💰 *Total:",
    "ai_title": "🤖 *AI Assistant*\n\n",
    "ai_desc": "Powered by FreeModel.dev (free).\n\n",
    "ai_usage": "Usage: `/ask what is DeFi?`\nExample: `/ask explain blockchain`",
    "ai_not_configured": "AI is not configured.\nSet `FREEMODEL_API_KEY` in .env",
    "ai_thinking": "🤔 Thinking...",
    "ai_error": "Error:",
    "price_usage": "Usage: `/price btc eth sol`\nExample: `/price bitcoin ethereum solana`",
    "price_error": "Error fetching prices.",
    "price_none": "No data found.",
    "alert_usage": "Usage: `/alert btc above 70000`\nExample: `/alert bitcoin above 70000`",
    "alert_direction": "Use `above` or `below`.",
    "alert_invalid": "Invalid price.",
    "alert_error": "Error fetching price.",
    "alert_not_found": "Coin `{}` not found.",
    "alert_triggered": "⚠️ *Alert triggered!*\n{} ${:,.2f} {} ${:,.2f}",
    "alert_not_triggered": "{} ${:,.2f}. Not {} ${:,.2f} yet.",
    "fng_error": "Error fetching Fear & Greed Index.",
    "news_none": "No news found.",
    "portfolio_added": "✅ Added {} {} to portfolio.",
    "portfolio_removed": "✅ Removed {} from portfolio.",
    "portfolio_not_found": "{} not in portfolio.",
    "add_usage": "Usage: `/add bitcoin 0.5`",
    "remove_usage": "Usage: `/remove bitcoin`",
    "add_invalid": "Invalid amount.",
    "whale_scanning": "🐋 Scanning...",
    "gas_fetching": "⛽ Fetching...",
    "lang_set": "🌐 Language set to English.",
    "lang_fa": "🌐 زبان به فارسی تغییر کرد.",
}
