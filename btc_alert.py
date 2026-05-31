import yfinance as yf

btc = yf.download(
    "BTC-USD",
    period="10d",
    interval="2h",
    auto_adjust=True
)

print(btc.tail())
print("Rows:", len(btc))
