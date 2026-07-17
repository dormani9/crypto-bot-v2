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

CHAINS = {
    "eth": {"id": 1, "label": "Ethereum"},
    "bsc": {"id": 56, "label": "BSC"},
    "polygon": {"id": 137, "label": "Polygon"},
    "arb": {"id": 42161, "label": "Arbitrum"},
    "op": {"id": 10, "label": "Optimism"},
    "base": {"id": 8453, "label": "Base"},
    "avax": {"id": 43114, "label": "Avalanche"},
    "cro": {"id": 25, "label": "Cronos"},
    "ftm": {"id": 250, "label": "Fantom"},
    "gnosis": {"id": 100, "label": "Gnosis"},
    "zksync": {"id": 324, "label": "zkSync Era"},
    "linea": {"id": 59144, "label": "Linea"},
    "scroll": {"id": 534352, "label": "Scroll"},
    "blast": {"id": 81457, "label": "Blast"},
    "mantle": {"id": 5000, "label": "Mantle"},
    "moonbeam": {"id": 1284, "label": "Moonbeam"},
    "celo": {"id": 42220, "label": "Celo"},
    "polygonzk": {"id": 1101, "label": "Polygon zkEVM"},
    "aurora": {"id": 1313161554, "label": "Aurora"},
    "metis": {"id": 1088, "label": "Metis"},
    "hyperevm": {"id": 999, "label": "HyperEVM"},
    "unichain": {"id": 130, "label": "Unichain"},
    "rhodefi": {"id": 4663, "label": "Robinhood Chain"},
}

CHAIN_ACTIONS = ["txlist", "tokentx"]


def _load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def _normalize_entry(entry):
    """Convert old format (string address) to new format (dict)."""
    if isinstance(entry, str):
        return {"address": entry, "chain": "eth"}
    return entry


def _tx_key(entry):
    """Unique key for last-tx tracking."""
    return f"{entry['address']}_{entry['chain']}"


async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not context.args:
        await update.message.reply_text(t["watch_usage"], parse_mode="Markdown")
        return

    address = context.args[0].lower()
    chain = context.args[1].lower() if len(context.args) > 1 else "eth"

    if not address.startswith("0x") or len(address) != 42:
        await update.message.reply_text(t["watch_invalid"], parse_mode="Markdown")
        return

    if chain not in CHAINS:
        lines = [t["watch_bad_chain"]]
        lines += [f"  `{k}` — {v['label']}" for k, v in CHAINS.items()]
        await update.message.reply_text("\n".join(lines), parse_mode="Markdown")
        return

    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    if uid_str not in data:
        data[uid_str] = []

    normalized = [_normalize_entry(e) for e in data[uid_str]]
    for e in normalized:
        if e["address"] == address and e["chain"] == chain:
            await update.message.reply_text(t["watch_exists"], parse_mode="Markdown")
            return

    entry = {"address": address, "chain": chain}
    normalized.append(entry)
    data[uid_str] = normalized
    _save_json(WATCH_FILE, data)

    label = CHAINS[chain]["label"]
    await update.message.reply_text(
        t["watch_added"].format(f"{address} ({label})"), parse_mode="Markdown"
    )


async def unwatch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    if not context.args:
        await update.message.reply_text(t["unwatch_usage"], parse_mode="Markdown")
        return

    address = context.args[0].lower()
    chain = context.args[1].lower() if len(context.args) > 1 else None

    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    if uid_str not in data:
        await update.message.reply_text(t["watch_not_found"], parse_mode="Markdown")
        return

    normalized = [_normalize_entry(e) for e in data[uid_str]]
    new_list = []
    removed = False
    for e in normalized:
        if e["address"] == address and (chain is None or e["chain"] == chain):
            removed = True
        else:
            new_list.append(e)

    if not removed:
        await update.message.reply_text(t["watch_not_found"], parse_mode="Markdown")
        return

    data[uid_str] = new_list
    if not new_list:
        del data[uid_str]
    _save_json(WATCH_FILE, data)
    label = f" ({CHAINS[chain]['label']})" if chain else ""
    await update.message.reply_text(
        t["unwatch_done"].format(f"{address}{label}"), parse_mode="Markdown"
    )


async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    data = _load_json(WATCH_FILE)
    uid_str = str(uid)
    entries = [_normalize_entry(e) for e in data.get(uid_str, [])]

    if not entries:
        await update.message.reply_text(t["wallets_empty"], parse_mode="Markdown")
        return

    lines = [t["wallets_title"]]
    for e in entries:
        short = e["address"][:10] + "..." + e["address"][-6:]
        label = CHAINS.get(e["chain"], {}).get("label", e["chain"])
        lines.append(f"🔹 `{short}` — {label}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


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


def _format_tx(tx: dict, address: str, chain_label: str) -> dict:
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
        value_label = f"{eth_value:.4f} {chain_label}"
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
        "chain_label": chain_label,
        "_address": address,
    }


def check_new_txs():
    if not ETHERSCAN_KEY:
        return {}

    data = _load_json(WATCH_FILE)
    last_tx = _load_json(LAST_TX_FILE)
    notifications = {}

    for uid_str, entries in data.items():
        for raw in entries:
            entry = _normalize_entry(raw)
            addr = entry["address"]
            chain_name = entry["chain"]
            chain_info = CHAINS.get(chain_name)
            if not chain_info:
                continue
            chain_label = chain_info["label"]
            chainid = chain_info["id"]

            all_txs = []
            seen_hashes = set()

            for action in CHAIN_ACTIONS:
                try:
                    txs = _fetch_txs(addr, chainid, action)
                    for tx in txs:
                        h = tx.get("hash", "")
                        if h and h not in seen_hashes:
                            seen_hashes.add(h)
                            all_txs.append((h, tx))
                except Exception as e:
                    logger.warning(f"{chain_name}/{action} failed for {addr}: {e}")
                    continue

            all_txs.sort(key=lambda x: int(x[1].get("timeStamp", 0) or 0), reverse=True)
            all_txs = all_txs[:5]

            if not all_txs:
                continue

            latest_hash = all_txs[0][0]
            tx_key = _tx_key(entry)
            prev_hash = last_tx.get(tx_key)
            new_items = []

            for h, tx in all_txs:
                if h == prev_hash:
                    break
                new_items.append(tx)
                if len(new_items) >= 2:
                    break

            if new_items:
                last_tx[tx_key] = latest_hash
                if prev_hash is not None:
                    if uid_str not in notifications:
                        notifications[uid_str] = []
                    for tx in new_items:
                        notifications[uid_str].append(
                            _format_tx(tx, addr, chain_label)
                        )
                else:
                    last_tx[tx_key] = latest_hash

    _save_json(LAST_TX_FILE, last_tx)
    return notifications


def get_handlers():
    return [
        CommandHandler("watch", watch),
        CommandHandler("unwatch", unwatch),
        CommandHandler("wallets", wallets),
    ]
