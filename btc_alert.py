import yfinance as yf
import pandas as pd

btc = yf.download(
    "BTC-USD",
    period="30d",
    interval="1h",
    auto_adjust=True
)

btc.columns = btc.columns.get_level_values(0)

btc["EMA200"] = btc["Close"].ewm(span=200).mean()

price = btc["Close"].iloc[-1]
ema200 = btc["EMA200"].iloc[-1]

print("Price:", round(price, 2))
print("EMA200:", round(ema200, 2))

if price > ema200:
    print("ABOVE EMA200")
else:
    print("BELOW EMA200")
