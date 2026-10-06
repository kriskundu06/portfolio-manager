import pandas as pd

INPUT_PATH = "data/processed/sp500_news_sentiment.csv"
OUTPUT_PATH = "data/processed/sp500_monthly_sentiment.csv"

df = pd.read_csv(INPUT_PATH)

df["Publishdate"] = pd.to_datetime(df["Publishdate"])

df["month"] = df["Publishdate"].dt.to_period("M").astype(str)

monthly = (
    df.groupby("month")["sentiment_score"]
    .mean()
    .reset_index()
)

monthly = monthly.rename(
    columns={"sentiment_score": "SP500_Sentiment"}
)

monthly.to_csv(OUTPUT_PATH, index=False)

print("S&P 500 monthly sentiment created.")
print(monthly.head())
print("\nShape:", monthly.shape)
print("\nDate range:", monthly["month"].min(), "to", monthly["month"].max())