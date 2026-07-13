import yfinance as yf

# Download stock data
stock = yf.download(
    "AAPL",
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)

# Flatten MultiIndex columns if present
if hasattr(stock.columns, "levels"):
    stock.columns = stock.columns.get_level_values(0)

# Save CSV
stock.to_csv("data/stock.csv", index=True)

print(stock.head())