import pandas as pd

MARKET_PATH = "data/processed/monthly_features.csv"

SP500_PATH = "data/processed/sp500_monthly_sentiment.csv"
GOLD_PATH = "data/processed/monthly_sentiment.csv"
OIL_PATH = "data/processed/oil_monthly_sentiment.csv"
NIFTY_PATH = "data/processed/nifty_monthly_sentiment.csv"

OUTPUT_PATH = "data/processed/monthly_features_sentiment.csv"

market = pd.read_csv(MARKET_PATH, index_col=0)

sp500 = pd.read_csv(SP500_PATH)
gold = pd.read_csv(GOLD_PATH)
oil = pd.read_csv(OIL_PATH)
nifty = pd.read_csv(NIFTY_PATH)

market["month"] = pd.to_datetime(market.index).to_period("M").astype(str)

sp500["month"] = sp500["month"].astype(str)
gold["month"] = gold["month"].astype(str)
oil["month"] = oil["month"].astype(str)
nifty["month"] = nifty["month"].astype(str)

market = market.reset_index(drop=True)

merged = market.merge(sp500, on="month", how="left")
merged = merged.merge(gold, on="month", how="left")
merged = merged.merge(oil, on="month", how="left")
merged = merged.merge(nifty, on="month", how="left")

sentiment_columns = [
    "SP500_Sentiment",
    "Gold_Sentiment",
    "OIL_Sentiment",
    "NIFTY_Sentiment"
]

merged[sentiment_columns] = merged[sentiment_columns].fillna(0)

merged.to_csv(OUTPUT_PATH, index=False)

print("Merged dataset created.")
print("Shape:", merged.shape)

print("\nColumns:")
print(merged.columns.tolist())

print("\nSentiment columns:")
print(merged[sentiment_columns].head())

print("\nDate range:")
print(merged["month"].min(), "to", merged["month"].max())

print("\nMissing sentiment values:")
print(merged[sentiment_columns].isna().sum())