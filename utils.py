import os
from typing import Optional, Tuple

import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
CG_API_KEY = os.getenv("COINGECKO_API_KEY")


def fetch_prices(coin_ids: list[str]) -> dict:
    ids = ",".join(c.lower() for c in coin_ids)
    params = {"ids": ids, "vs_currencies": "usd", "include_24hr_change": "true"}
    if CG_API_KEY:
        params["x_cg_demo_api_key"] = CG_API_KEY
    res = requests.get(COINGECKO_URL, params=params, timeout=10)
    res.raise_for_status()
    return res.json()


TOMAN_SOURCES = [
    {
        "name": "Nobitex",
        "url": "https://api.nobitex.ir/market/stats",
        "params": {"srcCurrency": "usdt"},
        "parse": lambda d: int(d["stats"]["usdt"]["latest"]),
    },
    {
        "name": "Wallex",
        "url": "https://api.wallex.ir/v1/markets",
        "parse": lambda d: int(float([m for m in d["result"] if m["symbol"] == "USDTIRT"][0]["price"])),
    },
    {
        "name": "Bit24",
        "url": "https://api.bit24.ir/api/v1/markets",
        "parse": lambda d: int(float([m for m in d if m["symbol"] == "USDTIRT"][0]["stats"]["last"])),
    },
]


def fetch_toman_price() -> Tuple[Optional[int], Optional[int], Optional[str]]:
    for src in TOMAN_SOURCES:
        try:
            params = src.get("params", {})
            res = requests.get(src["url"], params=params, timeout=8)
            res.raise_for_status()
            data = res.json()
            usdt_price = src["parse"](data)
            return usdt_price, usdt_price, src["name"]
        except Exception:
            continue
    return None, None, None
