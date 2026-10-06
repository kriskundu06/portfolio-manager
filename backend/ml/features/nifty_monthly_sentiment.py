import pandas as pd

INPUT_PATH = "backend/ml/data/data/raw/news/nifty/indic-finance.csv"
OUTPUT_PATH = "data/processed/nifty_monthly_sentiment.csv"

df = pd.read_csv(INPUT_PATH)

df["date"] = pd.to_datetime(df["date"], errors="coerce")

df = df.dropna(
    subset=["date", "sentiment_positive", "sentiment_negative"]
)

df["sentiment_score"] = (
    df["sentiment_positive"] - df["sentiment_negative"]
)

df["month"] = df["date"].dt.to_period("M").astype(str)

monthly = (
    df.groupby("month")["sentiment_score"]
    .mean()
    .reset_index()
)

monthly = monthly.rename(
    columns={"sentiment_score": "NIFTY_Sentiment"}
)

monthly.to_csv(OUTPUT_PATH, index=False)

print("NIFTY monthly sentiment created.")
print(monthly.head())
print("\nShape:", monthly.shape)
print(
    "\nDate range:",
    monthly["month"].min(),
    "to",
    monthly["month"].max()
)