import requests
import pandas as pd

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

params = {
    "vs_currency": "usd",
    "days": "30",
    "interval": "hourly"
}

data = requests.get(url, params=params).json()

prices = data["prices"]

df = pd.DataFrame(prices, columns=["timestamp", "close"])

df["EMA200"] = df["close"].ewm(span=200).mean()

print("Current Price:", round(df["close"].iloc[-1], 2))
print("EMA200:", round(df["EMA200"].iloc[-1], 2))
