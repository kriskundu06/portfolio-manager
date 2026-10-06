import pandas as pd

INPUT_PATH = "data/processed/oil_news_sentiment.csv"
OUTPUT_PATH = "data/processed/oil_monthly_sentiment.csv"

df = pd.read_csv(INPUT_PATH)

df["date"] = pd.to_datetime(df["date"])

df["month"] = df["date"].dt.to_period("M")

monthly = (
    df.groupby("month")["FinBERT_Sentiment"]
    .mean()
    .reset_index()
)

monthly["month"] = monthly["month"].astype(str)

monthly.rename(
    columns={"FinBERT_Sentiment": "OIL_Sentiment"},
    inplace=True
)

monthly.to_csv(OUTPUT_PATH, index=False)

print("Oil monthly sentiment created!")
print("Shape:", monthly.shape)
print("\nFirst 5 rows:")
print(monthly.head())