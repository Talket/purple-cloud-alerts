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
# ATR(10)
# =========================

tr1 = high - low
tr2 = abs(high - close.shift(1))
tr3 = abs(low - close.shift(1))

tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

atr = tr.rolling(10).mean()

# =========================
# Basic Bands
# =========================

factor = 3.0

hl2 = (high + low) / 2

upper_band = hl2 + factor * atr
lower_band = hl2 - factor * atr

# =========================
# Final Bands
# =========================

final_upper = upper_band.copy()
final_lower = lower_band.copy()

# Find first valid ATR value
first_valid = atr.first_valid_index()
start = btc.index.get_loc(first_valid)

# Initialize values before calculations begin
for i in range(start + 1):
    final_upper.iloc[i] = upper_band.iloc[i]
    final_lower.iloc[i] = lower_band.iloc[i]

# Calculate final bands
for i in range(start + 1, len(btc)):

    if (
        upper_band.iloc[i] < final_upper.iloc[i - 1]
        or close.iloc[i - 1] > final_upper.iloc[i - 1]
    ):
        final_upper.iloc[i] = upper_band.iloc[i]
    else:
        final_upper.iloc[i] = final_upper.iloc[i - 1]

    if (
        lower_band.iloc[i] > final_lower.iloc[i - 1]
        or close.iloc[i - 1] < final_lower.iloc[i - 1]
    ):
        final_lower.iloc[i] = lower_band.iloc[i]
    else:
        final_lower.iloc[i] = final_lower.iloc[i - 1]

# =========================
# Direction
# =========================

direction = pd.Series(index=btc.index, dtype=int)

direction.iloc[: start + 1] = 1

for i in range(start + 1, len(btc)):

    if close.iloc[i] > final_upper.iloc[i - 1]:
        direction.iloc[i] = 1

    elif close.iloc[i] < final_lower.iloc[i - 1]:
        direction.iloc[i] = -1

    else:
        direction.iloc[i] = direction.iloc[i - 1]

# =========================
# Output
# =========================

print("Price:", round(close.iloc[-1], 2))
print("ATR10:", round(atr.iloc[-1], 2))
print("Direction:", int(direction.iloc[-1]))
print("Final Upper:", round(final_upper.iloc[-1], 2))
print("Final Lower:", round(final_lower.iloc[-1], 2))
