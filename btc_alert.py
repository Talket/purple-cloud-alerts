import os
import requests
import ccxt

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

exchange = ccxt.bybit()

ticker = exchange.fetch_ticker("BTCUSDT")
price = ticker["last"]

message = f"BTC Price: ${price}"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": message
    }
)

print(message)
