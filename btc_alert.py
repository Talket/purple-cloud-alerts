import os
import requests
import pandas as pd

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

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

price = df["close"].iloc[-1]
ema200 = df["EMA200"].iloc[-1]

if price > ema200:
    message = f"🟢 BTC ABOVE EMA200\nPrice: {price:.2f}\nEMA200: {ema200:.2f}"
else:
    message = f"🔴 BTC BELOW EMA200\nPrice: {price:.2f}\nEMA200: {ema200:.2f}"

requests.post(
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
