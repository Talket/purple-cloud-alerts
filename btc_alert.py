import yfinance as yf
import pandas as pd
import numpy as np

btc = yf.download(
    "BTC-USD",
    period="30d",
    interval="1h",
    auto_adjust=True
)

btc.columns = btc.columns.get_level_values(0)

high = btc["High"]
low = btc["Low"]
close = btc["Close"]

tr1 = high - low
tr2 = abs(high - close.shift(1))
tr3 = abs(low - close.shift(1))

tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

btc["ATR40"] = tr.rolling(40).mean()

print("Price:", round(close.iloc[-1], 2))
print("ATR40:", round(btc["ATR40"].iloc[-1], 2))
