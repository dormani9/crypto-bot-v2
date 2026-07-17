import os

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
