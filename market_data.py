
import requests
import pandas as pd
from config import MARKET_SYMBOL, TIMEFRAME, MARKET_DATA_API_KEY, CANDLE_LIMIT


def get_market_data():
    if not MARKET_DATA_API_KEY:
        raise ValueError("MARKET_DATA_API_KEY is not configured.")

    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": MARKET_SYMBOL,
        "interval": TIMEFRAME,
        "outputsize": CANDLE_LIMIT,
        "apikey": MARKET_DATA_API_KEY,
        "format": "JSON",
    }

    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()

    data = response.json()

    if "values" not in data:
        raise ValueError(f"Market API error: {data}")

    df = pd.DataFrame(data["values"])

    for column in ["open", "high", "low", "close"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.sort_values("datetime").reset_index(drop=True)

    return df
