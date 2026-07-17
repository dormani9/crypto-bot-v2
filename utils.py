import logging
import os
from typing import Optional, Tuple

import requests

logger = logging.getLogger(__name__)

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
CG_API_KEY = os.getenv("COINGECKO_API_KEY")


COIN_ALIASES = {
    "btc": "bitcoin", "eth": "ethereum", "sol": "solana", "xrp": "ripple",
    "ada": "cardano", "dot": "polkadot", "ltc": "litecoin", "link": "chainlink",
    "matic": "matic-network", "avax": "avalanche-2", "bnb": "binancecoin",
    "doge": "dogecoin", "trx": "tron", "atom": "cosmos", "uni": "uniswap",
    "aave": "aave", "cro": "crypto-com-chain", "vet": "vechain",
    "theta": "theta-token", "fil": "filecoin", "icp": "internet-computer",
    "near": "near", "apt": "aptos", "sui": "sui", "arb": "arbitrum",
    "op": "optimism", "inj": "injective", "ldo": "lido-dao",
    "rune": "thorchain", "ftm": "fantom", "cake": "pancakeswap",
}


def fetch_prices(coin_ids: list[str]) -> dict:
    resolved = [COIN_ALIASES.get(c.lower(), c.lower()) for c in coin_ids]
    ids = ",".join(resolved)
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    if CG_API_KEY:
        params["x_cg_demo_api_key"] = CG_API_KEY
    res = requests.get(COINGECKO_URL, params=params, timeout=10)
    res.raise_for_status()
    return res.json()


IRR_SOURCES = [
    {
        "name": "ExchangeRate-API",
        "url": "https://open.er-api.com/v6/latest/USD",
        "parse": lambda d: int(float(d["rates"]["IRR"])),
    },
]


def fetch_toman_price() -> Tuple[Optional[int], Optional[int], Optional[str]]:
    # First try Iranian exchange APIs
    iranian_sources = [
        {
            "name": "Wallex",
            "url": "https://api.wallex.ir/v1/markets",
            "parse": lambda d: int(float(d["result"]["symbols"]["USDTTMN"]["stats"]["lastPrice"])),
        },
        {
            "name": "Nobitex",
            "url": "https://api.nobitex.ir/market/stats",
            "params": {"srcCurrency": "usdt"},
            "parse": lambda d: int(d["stats"]["usdt"]["latest"]),
        },
    ]

    for src in iranian_sources:
        try:
            params = src.get("params", {})
            res = requests.get(src["url"], params=params, timeout=5)
            res.raise_for_status()
            data = res.json()
            price = src["parse"](data)
            logger.info(f"USDT/IRR via {src['name']}: {price}")
            return price, price, src["name"]
        except Exception as e:
            logger.warning(f"{src['name']} failed: {e}")
            continue

    # Fallback: CoinGecko + ExchangeRate-API
    try:
        cg = requests.get(
            COINGECKO_URL,
            params={"ids": "tether", "vs_currencies": "usd"},
            timeout=8,
        )
        usdt_usd = cg.json().get("tether", {}).get("usd", 1)

        for src in IRR_SOURCES:
            res = requests.get(src["url"], timeout=8)
            res.raise_for_status()
            data = res.json()
            irr_per_usd = src["parse"](data)
            toman_per_usd = irr_per_usd // 10  # 10 IRR = 1 Toman
            usdt_toman = int(usdt_usd * toman_per_usd)
            logger.info(f"USDT/Toman via fallback: {usdt_toman}")
            return usdt_toman, toman_per_usd, f"{src['name']} + CoinGecko"
    except Exception as e:
        logger.error(f"Fallback failed: {e}")

    return None, None, None
