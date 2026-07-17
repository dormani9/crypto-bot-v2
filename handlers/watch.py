import json
import logging
import os
from pathlib import Path

import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from lang import EN, FA, get_lang

WATCH_FILE = Path(__file__).parent.parent / "wallet-monitor.json"
LAST_BLOCK_FILE = Path(__file__).parent.parent / "last-block.json"
ETHERSCAN_KEY = os.getenv("ETHERSCAN_API_KEY")
BLOCKSCOUT_KEY = os.getenv("BLOCKSCOUT_API_KEY")

logger = logging.getLogger(__name__)

CHAINS = {
    "eth": {"id": 1, "label": "Ethereum", "api": "etherscan"},
    "bsc": {"id": 56, "label": "BSC", "api": "etherscan"},
    "polygon": {"id": 137, "label": "Polygon", "api": "etherscan"},
    "arb": {"id": 42161, "label": "Arbitrum", "api": "etherscan"},
    "op": {"id": 10, "label": "Optimism", "api": "etherscan"},
    "base": {"id": 8453, "label": "Base", "api": "etherscan"},
    "avax": {"id": 43114, "label": "Avalanche", "api": "etherscan"},
    "cro": {"id": 25, "label": "Cronos", "api": "etherscan"},
    "ftm": {"id": 250, "label": "Fantom", "api": "etherscan"},
    "gnosis": {"id": 100, "label": "Gnosis", "api": "etherscan"},
    "zksync": {"id": 324, "label": "zkSync Era", "api": "etherscan"},
    "linea": {"id": 59144, "label": "Linea", "api": "etherscan"},
    "scroll": {"id": 534352, "label": "Scroll", "api": "etherscan"},
    "blast": {"id": 81457, "label": "Blast", "api": "etherscan"},
    "mantle": {"id": 5000, "label": "Mantle", "api": "etherscan"},
    "moonbeam": {"id": 1284, "label": "Moonbeam", "api": "etherscan"},
    "celo": {"id": 42220, "label": "Celo", "api": "etherscan"},
    "polygonzk": {"id": 1101, "label": "Polygon zkEVM", "api": "etherscan"},
    "aurora": {"id": 1313161554, "label": "Aurora", "api": "etherscan"},
    "metis": {"id": 1088, "label": "Metis", "api": "etherscan"},
    "hyperevm": {"id": 999, "label": "HyperEVM", "api": "etherscan"},
    "unichain": {"id": 130, "label": "Unichain", "api": "etherscan"},
    "rhodefi": {"id": 4663, "label": "Robinhood Chain", "api": "blockscout"},
}

FALLBACK_CHAINS = {}  # chains where etherscan is paid-only; we use blockscout instead


def _load_json(path):
    if path.exists():
        return json.loads(path.read_text())
    return {}


def _save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def _normalize(entry):
    if isinstance(entry, str):
        return {"address": entry, "chain": "eth"}
    return entry


def _key(entry, chain_name=None):
    e = _normalize(entry)
    c = chain_name or e["chain"]
    return f"{e['address']}_{c}"


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
    normalized = [_normalize(e) for e in data.get(uid_str, [])]
    for e in normalized:
        if e["address"] == address and e["chain"] == chain:
            await update.message.reply_text(t["watch_exists"], parse_mode="Markdown")
            return

    entry = {"address": address, "chain": chain}
    normalized.append(entry)
    data[uid_str] = normalized
    _save_json(WATCH_FILE, data)

    # Remove old last-block entry so next check treats it as first-run
    bk = _key(entry)
    blocks = _load_json(LAST_BLOCK_FILE)
    blocks.pop(bk, None)
    _save_json(LAST_BLOCK_FILE, blocks)

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

    normalized = [_normalize(e) for e in data[uid_str]]
    new_list = []
    removed = []
    for e in normalized:
        if e["address"] == address and (chain is None or e["chain"] == chain):
            removed.append(e)
        else:
            new_list.append(e)

    if not removed:
        await update.message.reply_text(t["watch_not_found"], parse_mode="Markdown")
        return

    data[uid_str] = new_list
    if not new_list:
        del data[uid_str]
    _save_json(WATCH_FILE, data)

    # Also clean up last-block entries
    blocks = _load_json(LAST_BLOCK_FILE)
    for e in removed:
        blocks.pop(_key(e), None)
    _save_json(LAST_BLOCK_FILE, blocks)

    parts = [address]
    if chain:
        parts.append(f"({CHAINS[chain]['label']})")
    await update.message.reply_text(
        t["unwatch_done"].format(" ".join(parts)), parse_mode="Markdown"
    )


async def wallets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN

    data = _load_json(WATCH_FILE)
    entries = [_normalize(e) for e in data.get(str(uid), [])]

    if not entries:
        await update.message.reply_text(t["wallets_empty"], parse_mode="Markdown")
        return

    lines = [t["wallets_title"]]
    for e in entries:
        short = e["address"][:10] + "..." + e["address"][-6:]
        label = CHAINS.get(e["chain"], {}).get("label", e["chain"])
        lines.append(f"🔹 `{short}` — {label}")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def _fetch(address, chain_name):
    """Fetch latest normal tx + token tx for a wallet on a chain."""
    chain = CHAINS[chain_name]
    chainid = chain["id"]
    api = chain.get("api", "etherscan")

    if api == "blockscout":
        key = os.getenv("BLOCKSCOUT_API_KEY")
        base = "https://api.blockscout.com/v2/api"
        cid_param = "chain_id"
    else:
        key = os.getenv("ETHERSCAN_API_KEY")
        base = "https://api.etherscan.io/v2/api"
        cid_param = "chainid"

    out = []
    for action in ("txlist", "tokentx"):
        try:
            params = {cid_param: chainid, "module": "account", "action": action, "address": address, "sort": "desc", "offset": 3}
            if key:
                params["apikey"] = key
            r = requests.get(base, params=params, timeout=12)
            items = r.json().get("result", [])
            if isinstance(items, list):
                out.extend(items)
        except Exception as e:
            logger.warning(f"_fetch {chain_name}/{action} {address[:10]}: {e}")
    return out


def format_tx(tx, address, chain_label):
    value_raw = int(tx.get("value", 0))
    is_token = "tokenSymbol" in tx
    if is_token:
        sym = tx.get("tokenSymbol", "?")
        dec = int(tx.get("tokenDecimal", 18))
        val = value_raw / (10 ** dec)
        label = f"{val:,.4f} {sym}"
    else:
        val = value_raw / 1e18
        label = f"{val:.4f} {chain_label}"
    return {
        "hash": tx.get("hash", ""),
        "label": label,
        "from": tx.get("from", ""),
        "to": tx.get("to", ""),
        "block": int(tx.get("blockNumber", 0) or 0),
        "is_token": is_token,
        "chain": chain_label,
        "address": address,
    }


def check_new_txs():
    if not ETHERSCAN_KEY and not BLOCKSCOUT_KEY:
        logger.warning("check_new_txs: no API keys set")
        return {}

    data = _load_json(WATCH_FILE)
    if not data:
        logger.info("check_new_txs: no wallets in file")
        return {}

    total_wallets = sum(len(v) for v in data.values())
    logger.info(f"check_new_txs: {total_wallets} wallet(s) for {len(data)} user(s)")
    blocks = _load_json(LAST_BLOCK_FILE)
    out = {}

    for uid_str, entries in data.items():
        for raw in entries:
            entry = _normalize(raw)
            addr = entry["address"]
            cn = entry["chain"]
            ci = CHAINS.get(cn)
            if not ci:
                logger.warning(f"check_new_txs: unknown chain {cn} for {addr[:10]}")
                continue
            cl = ci["label"]

            txs = _fetch(addr, cn)
            if not txs:
                logger.info(f"check {addr[:10]}@{cn}: no txs returned (API error or empty)")
                continue

            # collect unique hashes, find max block
            seen = set()
            latest_block = 0
            new_txs = []
            for tx in sorted(txs, key=lambda x: int(x.get("blockNumber", 0) or 0), reverse=True):
                h = tx.get("hash", "")
                if not h or h in seen:
                    continue
                seen.add(h)
                bn = int(tx.get("blockNumber", 0) or 0)
                if bn > latest_block:
                    latest_block = bn
                new_txs.append(tx)

            if not latest_block:
                logger.info(f"check {addr[:10]}@{cn}: no block number in txs")
                continue

            base_k = _key(entry)
            prev_block = blocks.get(base_k, 0)
            logger.info(f"check {addr[:10]}@{cn}: prev_block={prev_block}, latest_block={latest_block}")

            if prev_block == 0:
                # first run — just remember the block
                blocks[base_k] = latest_block
                logger.info(f"check {addr[:10]}@{cn}: first run, stored block {latest_block}")
                continue

            if latest_block <= prev_block:
                logger.info(f"check {addr[:10]}@{cn}: no new blocks")
                continue

            # find txs with block > prev_block (up to 3)
            fresh = []
            for tx in new_txs:
                bn = int(tx.get("blockNumber", 0) or 0)
                if bn > prev_block:
                    fresh.append(tx)
                    if len(fresh) >= 3:
                        break

            if fresh:
                blocks[base_k] = latest_block
                if uid_str not in out:
                    out[uid_str] = []
                for tx in fresh:
                    out[uid_str].append(format_tx(tx, addr, cl))
                logger.info(f"check {addr[:10]}@{cn}: {len(fresh)} new tx(s) (block {prev_block}→{latest_block})")
            else:
                logger.info(f"check {addr[:10]}@{cn}: latest_block>{prev_block} but no fresh tx after filter")

    _save_json(LAST_BLOCK_FILE, blocks)
    return out


async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manual check — call /check to force a wallet scan right now."""
    uid = update.effective_user.id
    t = FA if get_lang(uid) == "fa" else EN
    msg = await update.message.reply_text("🔍 Scanning wallets...")
    try:
        result = check_new_txs()
        my_txs = result.get(str(uid), [])
        if not my_txs:
            await msg.edit_text("✅ No new transactions found.")
        else:
            from main import _send_wallet_notification
            for tx in my_txs:
                await _send_wallet_notification(uid, tx, context)
            await msg.edit_text(f"✅ Sent {len(my_txs)} notification(s).")
    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")


def get_handlers():
    return [
        CommandHandler("watch", watch),
        CommandHandler("unwatch", unwatch),
        CommandHandler("wallets", wallets),
        CommandHandler("check", check),
    ]
