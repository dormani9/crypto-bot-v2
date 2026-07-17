import json
import logging
import os
from pathlib import Path

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from lang import EN, FA, get_lang

WATCH_FILE = Path(__file__).parent.parent / "wallet-monitor.json"
LAST_TX_FILE = Path(__file__).parent.parent / "last-tx.json"
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
ETHERSCAN_V2 = "https://api.etherscan.io/v2/api"

logger = logging.getLogger(__name__)


def _load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not context.args:
        await update.message.reply_text(t["watch_usage"], parse_mode="Markdown")
        return

    address = context.args[0]
    if not address.startswith("0x") or len(address) != 42:
        await update.message.reply_text(t["watch_invalid"], parse_mode="Markdown")
        return

    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    if uid_str not in data:
        data[uid_str] = []
    if address in data[uid_str]:
        await update.message.reply_text(t["watch_exists"], parse_mode="Markdown")
        return
    data[uid_str].append(address)
    _save_json(WATCH_FILE, data)
    await update.message.reply_text(
        t["watch_added"].format(address), parse_mode="Markdown"
    )


async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not context.args:
        await update.message.reply_text(t["unwatch_usage"], parse_mode="Markdown")
        return

    address = context.args[0].lower()
    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    if uid_str not in data or address not in data[uid_str]:
        await update.message.reply_text(t["watch_not_found"], parse_mode="Markdown")
        return
    data[uid_str].remove(address)
    if not data[uid_str]:
        del data[uid_str]
    _save_json(WATCH_FILE, data)
    await update.message.reply_text(
        t["unwatch_done"].format(address), parse_mode="Markdown"
    )


async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    addrs = data.get(uid_str, [])

    if not addrs:
        await update.message.reply_text(t["wallets_empty"], parse_mode="Markdown")
        return

    lines = [t["wallets_title"]]
    for addr in addrs:
        short = addr[:10] + "..." + addr[-6:]
        lines.append(f"🔹 `{short}` — `{addr}`")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


CHAIN_ACTIONS = [
    ("ETH", 1, "txlist"),
    ("ETH", 1, "tokentx"),
]


def _fetch_txs(address: str, chainid: int, action: str):
    params = {
        "chainid": chainid,
        "module": "account",
        "action": action,
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "desc",
        "page": 1,
        "offset": 5,
        "apikey": ETHERSCAN_KEY,
    }
    res = requests.get(ETHERSCAN_V2, params=params, timeout=10)
    txs = res.json().get("result", [])
    return txs if isinstance(txs, list) else []


def _format_tx(tx: dict, address: str) -> dict:
    """Normalize both ETH txlist and tokentx entries into a uniform dict."""
    value_raw = int(tx.get("value", 0))
    is_token = "tokenSymbol" in tx

    if is_token:
        token_symbol = tx.get("tokenSymbol", "?")
        token_decimal = int(tx.get("tokenDecimal", 18))
        token_value = value_raw / (10 ** token_decimal)
        value_label = f"{token_value:,.4f} {token_symbol}"
        usd_value = None
        tx_hash = tx.get("hash", "")
    else:
        eth_value = value_raw / 1e18
        value_label = f"{eth_value:.4f} ETH"
        usd_value = eth_value
        tx_hash = tx.get("hash", "")

    return {
        "hash": tx_hash,
        "value_label": value_label,
        "usd_value": usd_value,
        "from": tx.get("from", ""),
        "to": tx.get("to", ""),
        "is_token": is_token,
        "token_symbol": tx.get("tokenSymbol"),
        "_address": address,
    }


def check_new_txs():
    if not ETHERSCAN_KEY:
        return {}

    data = _load_json(WATCH_FILE)
    last_tx = _load_json(LAST_TX_FILE)
    notifications = {}

    for uid_str, addresses in data.items():
        for address in addresses:
            all_txs = []
            seen_hashes = set()

            for chain_name, chainid, action in CHAIN_ACTIONS:
                try:
                    txs = _fetch_txs(address, chainid, action)
                    for tx in txs:
                        h = tx.get("hash", "")
                        if h and h not in seen_hashes:
                            seen_hashes.add(h)
                            all_txs.append((h, tx))
                except Exception as e:
                    logger.warning(f"{chain_name}/{action} failed for {address}: {e}")
                    continue

            all_txs.sort(key=lambda x: int(x[1].get("timeStamp", 0) or 0), reverse=True)
            all_txs = all_txs[:5]

            if not all_txs:
                continue

            latest_hash = all_txs[0][0]
            prev_hash = last_tx.get(address)
            new_items = []

            for h, tx in all_txs:
                if h == prev_hash:
                    break
                new_items.append(tx)
                if len(new_items) >= 2:
                    break

            if new_items:
                last_tx[address] = latest_hash
                if prev_hash is not None:
                    if uid_str not in notifications:
                        notifications[uid_str] = []
                    for tx in new_items:
                        notifications[uid_str].append(_format_tx(tx, address))
                else:
                    last_tx[address] = latest_hash

    _save_json(LAST_TX_FILE, last_tx)
    return notifications


def get_handlers():
    return [
        CommandHandler("watch", watch),
        CommandHandler("unwatch", unwatch),
        CommandHandler("wallets", wallets),
    ]
