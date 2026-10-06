import pandas as pd


INPUT_PATH = "data/processed/monthly_features_sentiment.csv"

OUTPUT_PATH = "data/processed/monthly_features_sentiment_v2.csv"


SENTIMENT_COLUMNS = [
    "SP500_Sentiment",
    "Gold_Sentiment",
    "OIL_Sentiment",
    "NIFTY_Sentiment"
]


df = pd.read_csv(INPUT_PATH)

df["month"] = pd.to_datetime(df["month"])

df = df.sort_values("month").reset_index(drop=True)


for column in SENTIMENT_COLUMNS:

    df[f"{column}_3m_avg"] = (
        df[column]
        .rolling(window=3, min_periods=1)
        .mean()
    )

    df[f"{column}_momentum"] = (
        df[column]
        - df[f"{column}_3m_avg"]
    )


df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("Sentiment features v2 created.")
print("Shape:", df.shape)
print("Saved to:", OUTPUT_PATH)

print("\nNew sentiment columns:")

for column in SENTIMENT_COLUMNS:
    print(column)
    print(f"  {column}_3m_avg")
    print(f"  {column}_momentum")