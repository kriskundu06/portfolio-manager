import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "ProsusAI/finbert"

INPUT_PATH = "backend/ml/data/data/raw/news/oil/oil_sentiment_headlines.csv"
OUTPUT_PATH = "data/processed/oil_news_sentiment.csv"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()

df = pd.read_csv(INPUT_PATH)

news = df["headline"].fillna("").tolist()

batch_size = 32
sentiment_scores = []

for start in range(0, len(news), batch_size):

    batch = news[start:start + batch_size]

    inputs = tokenizer(
        batch,
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    positive = probabilities[:, 0]
    negative = probabilities[:, 1]

    scores = positive - negative

    sentiment_scores.extend(scores.tolist())

    print(
        f"Processed {min(start + batch_size, len(news))}/{len(news)}"
    )

df["FinBERT_Sentiment"] = sentiment_scores

df.to_csv(OUTPUT_PATH, index=False)

print("\nDone!")
print("Saved to:", OUTPUT_PATH)
print("Rows:", len(df))