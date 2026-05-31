import requests

url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"

params = {
    "vs_currency": "usd",
    "days": "7",
    "interval": "hourly"
}

data = requests.get(url, params=params).json()

prices = data["prices"]

print(f"Downloaded {len(prices)} candles")
print(prices[-1])
