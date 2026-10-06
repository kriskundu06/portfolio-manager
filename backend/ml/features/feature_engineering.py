import pandas as pd
from pathlib import Path
RAW_DATA_PATH = Path("data/raw/daily_adj_close.csv")
PROCESSED_DATA_DIR = Path("data/processed")
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
def calculate_returns():

    print("Loading price data...")

    prices = pd.read_csv(
        RAW_DATA_PATH,
        index_col="Date",
        parse_dates=True
    )

    print("Price data loaded.")
    print(f"Shape: {prices.shape}")
    print("\nLast 5 price values:")
    print(prices.tail())
    returns = prices.pct_change(fill_method=None)
    returns = returns.dropna(how="all")
    output_path = PROCESSED_DATA_DIR / "daily_returns.csv"
    returns.to_csv(output_path)
    print("\nDaily returns calculated.")
    print("Saved to:", output_path)
    print("\nFirst 5 rows of returns:")
    print(returns.head())
    print("\nLast 5 rows of returns:")
    print(returns.tail())
if __name__ == "__main__":
    calculate_returns()