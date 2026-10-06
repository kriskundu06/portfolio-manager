import pandas as pd

path = "backend/ml/data/data/raw/news/oil/oil_sentiment_headlines.csv"

df = pd.read_csv(path)

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())