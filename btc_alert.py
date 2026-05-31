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

# True Range
tr1 = high - low
tr2 = abs(high - close.shift(1))
tr3 = abs(low - close.shift(1))

tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

# ATR 10 (same as your Pine Script)
atr = tr.rolling(10).mean()

btc["ATR10"] = atr

print("Price:", round(close.iloc[-1], 2))
print("ATR10:", round(atr.iloc[-1], 2))
