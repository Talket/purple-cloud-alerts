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

# =========================
# ATR 10
# =========================

tr1 = high - low
tr2 = abs(high - close.shift(1))
tr3 = abs(low - close.shift(1))

tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

atr = tr.rolling(10).mean()

btc["ATR10"] = atr

# =========================
# Supertrend Basic Bands
# =========================

factor = 3.0

hl2 = (high + low) / 2

upper_band = hl2 + factor * atr
lower_band = hl2 - factor * atr

btc["UpperBand"] = upper_band
btc["LowerBand"] = lower_band

print("Price:", round(close.iloc[-1], 2))
print("ATR10:", round(atr.iloc[-1], 2))
print("Upper Band:", round(upper_band.iloc[-1], 2))
print("Lower Band:", round(lower_band.iloc[-1], 2))
