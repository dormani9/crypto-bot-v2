import json
import os
from pathlib import Path

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, filters

DATA_FILE = Path(__file__).parent.parent / "portfolio.json"


def _load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {}


def _save(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


async def portfolio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = _load()
    if not data:
        await update.message.reply_text(
            "Portfolio is empty.\n"
            "Add: `/add bitcoin 0.5`\n"
            "Remove: `/remove bitcoin`",
            parse_mode="Markdown",
        )
        return

    ids = ",".join(data.keys())
    try:
        res = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": ids, "vs_currencies": "usd"},
            timeout=10,
        )
        prices = res.json()
    except Exception:
        await update.message.reply_text("Error fetching prices.")
        return

    total = 0
    lines = ["💼 *Portfolio*\n"]
    for coin_id, amount in sorted(data.items()):
        price = prices.get(coin_id, {}).get("usd", 0)
        value = amount * price
        total += value
        lines.append(f"• {coin_id.title()}: {amount} → `${value:,.2f}`")

    lines.append(f"\n💰 *Total: ${total:,.2f}*")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: `/add bitcoin 0.5`", parse_mode="Markdown")
        return

    coin, amount_str = context.args[0].lower(), context.args[1]
    try:
        amount = float(amount_str)
    except ValueError:
        await update.message.reply_text("Invalid amount.")
        return

    data = _load()
    data[coin] = data.get(coin, 0) + amount
    _save(data)
    await update.message.reply_text(f"✅ Added {amount} {coin.title()}")


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/remove bitcoin`", parse_mode="Markdown")
        return

    coin = context.args[0].lower()
    data = _load()
    if coin not in data:
        await update.message.reply_text(f"{coin.title()} not in portfolio.")
        return

    del data[coin]
    _save(data)
    await update.message.reply_text(f"✅ Removed {coin.title()}")


def get_handlers():
    return [
        CommandHandler("portfolio", portfolio, filters.TEXT),
        CommandHandler("add", add, filters.TEXT),
        CommandHandler("remove", remove, filters.TEXT),
    ]
