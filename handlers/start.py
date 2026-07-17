from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes, filters

from lang import EN, FA, get_lang, set_lang


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
            InlineKeyboardButton("🇮🇷 فارسی", callback_data="lang_fa"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🌐 *Select your language / زبان خود را انتخاب کنید:*\n\n"
        "🇬🇧 English  —  🇮🇷 فارسی",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    lang = get_lang(uid)
    t = FA if lang == "fa" else EN

    keyboard = [
        [
            InlineKeyboardButton(t["price"], callback_data="menu_price"),
            InlineKeyboardButton(t["fng"], callback_data="menu_fng"),
        ],
        [
            InlineKeyboardButton("💱 Toman" if lang == "en" else "💱 تومان", callback_data="menu_toman"),
            InlineKeyboardButton(t["news"], callback_data="menu_news"),
        ],
        [
            InlineKeyboardButton(t["whale"], callback_data="menu_whale"),
            InlineKeyboardButton(t["gas"], callback_data="menu_gas"),
        ],
        [
            InlineKeyboardButton(t["portfolio"], callback_data="menu_portfolio"),
            InlineKeyboardButton(t["ai"], callback_data="menu_ai"),
        ],
    ]
    await query.edit_message_text(t["menu_title"], parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))


async def lang_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = update.effective_user.id
    lang = "fa" if query.data == "lang_fa" else "en"
    set_lang(uid, lang)
    await show_main_menu(update, context)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    lang = get_lang(uid)
    t = FA if lang == "fa" else EN

    text = t["help_title"]
    text += t["help_price"]
    text += t["help_alert"]
    text += t["help_fng"]
    text += t["help_news"]
    text += t["help_fnews"]
    text += t["help_whale"]
    text += t["help_gas"]
    text += t["help_wallet"]
    text += t["help_ask"]
    text += t["help_watch"]

    if lang == "fa":
        text += "\n🌐 `/lang` — تغییر زبان"

    await update.message.reply_text(text, parse_mode="Markdown")


async def lang_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    current = get_lang(uid)
    new_lang = "fa" if current != "fa" else "en"
    set_lang(uid, new_lang)
    t = FA if new_lang == "fa" else EN
    await update.message.reply_text(t["lang_set"])


def get_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("help", help_cmd),
        CommandHandler("lang", lang_cmd),
    ]


def get_callback_handlers():
    return [CallbackQueryHandler(lang_callback, pattern="^lang_")]
