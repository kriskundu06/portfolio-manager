import yfinance as yf
import pandas as pd
from pathlib import Path
import time
TICKERS = {
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "GOLD": "GC=F",
    "OIL": "CL=F",
    "NIFTY": "^NSEI"
}

START_DATE = "2005-01-01"
END_DATE = "2026-01-01"

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "daily_adj_close.csv"
def download_data():
    print("Downloading market data from Yahoo Finance...\n")
    all_data = {}
    for name, ticker in TICKERS.items():
        print(f"Downloading {name} ({ticker})...")
        success = False
        for attempt in range(3):
            try:
                data = yf.download(
                    ticker,
                    start=START_DATE,
                    end=END_DATE,
                    interval="1d",
                    auto_adjust=False,
                    progress=False,
                    threads=False
                )
                if data.empty:
                    raise ValueError("No data returned")
                adj_close = data["Adj Close"]
                if isinstance(adj_close, pd.DataFrame):
                    adj_close = adj_close.iloc[:, 0]
                adj_close = adj_close.dropna()
                if len(adj_close) == 0:
                    raise ValueError("Adjusted Close contains no valid values")
                all_data[name] = adj_close
                print(
                    f"{name} downloaded successfully "
                    f"({len(adj_close)} valid values).\n"
                )
                success = True
                break

            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    print("Retrying in 3 seconds...\n")
                    time.sleep(3)
        if not success:
            print(f"\nERROR: Could not download {name}.")
            print("Dataset was NOT saved.")
            return
    print("\nAll assets downloaded successfully.")
    prices = pd.DataFrame(all_data)
    prices = prices.sort_index()
    print("\nValid values per asset:")
    print(prices.notna().sum())
    print("\nFirst 5 rows:")
    print(prices.head())
    print("\nLast 5 rows:")
    print(prices.tail())
    prices.to_csv(OUTPUT_PATH)
    print("\nData saved to:")
    print(OUTPUT_PATH)
    print("\nFinal shape:")
    print(prices.shape)

if __name__ == "__main__":
    download_data()