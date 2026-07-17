from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, ContextTypes, filters


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("💰 Price", callback_data="menu_price"),
            InlineKeyboardButton("😱 F&G Index", callback_data="menu_fng"),
        ],
        [
            InlineKeyboardButton("📰 News", callback_data="menu_news"),
            InlineKeyboardButton("🐋 Whale Alert", callback_data="menu_whale"),
        ],
        [
            InlineKeyboardButton("⛽ Gas Fee", callback_data="menu_gas"),
            InlineKeyboardButton("💼 Portfolio", callback_data="menu_portfolio"),
        ],
        [
            InlineKeyboardButton("🤖 AI Assistant", callback_data="menu_ai"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚀 *Crypto Bot v2*\n\n"
        "Your all-in-one cryptocurrency companion.\n"
        "Use the menu below or type /help for commands.\n\n"
        "✨ *New:* Free AI assistant powered by Gemini!",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📚 *Commands*\n\n"
        "`/price btc eth` — current prices\n"
        "`/alert btc above 70000` — price check\n"
        "`/fng` — Fear & Greed Index\n"
        "`/news 5` — English news\n"
        "`/fnews 5` — اخبار فارسی\n"
        "`/whale` — large transactions\n"
        "`/gas` — Ethereum gas fees\n"
        "`/add btc 0.5` / `/portfolio` — track holdings\n"
        "`/ask what is eth` — AI assistant",
        parse_mode="Markdown",
    )


def get_handlers():
    return [
        CommandHandler("start", start, filters.TEXT),
        CommandHandler("help", help_cmd, filters.TEXT),
    ]
