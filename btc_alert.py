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
# Supertrend Line
# =========================

supertrend = pd.Series(index=btc.index, dtype=float)

for i in range(len(btc)):
    if direction.iloc[i] == 1:
        supertrend.iloc[i] = final_lower.iloc[i]
    else:
        supertrend.iloc[i] = final_upper.iloc[i]

btc["Supertrend"] = supertrend


# =========================
# EMA200
# =========================

ema200 = close.ewm(span=200, adjust=False).mean()

# =========================
# Purple Cloud Parameters
# =========================

x1 = 40
alpha = 0.9

# =========================
# ATR(40) * Alpha
# =========================

atr40 = tr.rolling(x1).mean()

x2 = atr40 * alpha

xh = close + x2
xl = close - x2

# =========================
# Purple Cloud VWMA Logic
# =========================

volume = btc["Volume"]

len1 = int(np.ceil(x1 / 4))
len2 = int(np.ceil(x1 / 2))

# Pine:
# a1 = vwma(hl2*volume,len1)/vwma(volume,len1)

hl2 = (high + low) / 2

a1_num = (hl2 * volume).rolling(len1).sum()
a1_den = volume.rolling(len1).sum()

a1 = a1_num / a1_den

a2_num = (hl2 * volume).rolling(len2).sum()
a2_den = volume.rolling(len2).sum()

a2 = a2_num / a2_den

a3 = 2 * a1 - a2

# a4 = vwma(a3,40)

a3_filled = a3.ffill()

a4_num = (a3_filled * volume).rolling(x1).sum()
a4_den = volume.rolling(x1).sum()

a4 = a4_num / a4_den

# =========================
# b1
# =========================

b1 = close.ewm(alpha=(1 / x1), adjust=False).mean()

# =========================
# a5
# =========================

a5 = (2 * a4 * b1) / (a4 + b1)

# =========================
# Purple Cloud Signals
# =========================

bpt = 0.5
spt = 0.5

buy = (
    (a5 <= xl)
    & (close > b1 * (1 + bpt * 0.01))
)

sell = (
    (a5 >= xh)
    & (close < b1 * (1 - spt * 0.01))
)

# =========================
# XS State
# =========================

xs = pd.Series(index=btc.index, dtype=int)

xs.iloc[0] = 0

for i in range(1, len(btc)):

    if buy.iloc[i]:
        xs.iloc[i] = 1

    elif sell.iloc[i]:
        xs.iloc[i] = -1

    else:
        xs.iloc[i] = xs.iloc[i - 1]

# =========================
# Long / Short Conditions
# =========================

xs_prev = xs.shift(1)

long_condition = (
    buy
    & (xs != xs_prev)
    & (direction < 0)
)

short_condition = (
    sell
    & (xs != xs_prev)
    & (direction > 0)
)

# =========================
# EMA200 Filter
# =========================

buy_above_ema = (
    long_condition
    & (close > ema200)
)

short_below_ema = (
    short_condition
    & (close < ema200)
)

# =========================
# Output
# =========================

print("Price:", round(close.iloc[-1], 2))
print("EMA200:", round(ema200.iloc[-1], 2))

print("Direction:", int(direction.iloc[-1]))
print("Supertrend:", round(supertrend.iloc[-1], 2))

print("a5:", round(a5.iloc[-1], 2))
print("b1:", round(b1.iloc[-1], 2))

print("xh:", round(xh.iloc[-1], 2))
print("xl:", round(xl.iloc[-1], 2))

print("Buy:", bool(buy.iloc[-1]))
print("Sell:", bool(sell.iloc[-1]))

print("XS:", int(xs.iloc[-1]))

print("Long Condition:", bool(long_condition.iloc[-1]))
print("Short Condition:", bool(short_condition.iloc[-1]))

print("BUY Above EMA200:", bool(buy_above_ema.iloc[-1]))
print("SHORT Below EMA200:", bool(short_below_ema.iloc[-1]))
