import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

INPUT_PATH = "backend/ml/data/data/raw/news/sp500/stock_data_articles.jsonl"
OUTPUT_PATH = "data/processed/sp500_news_sentiment.csv"

MODEL_NAME = "ProsusAI/finbert"
BATCH_SIZE = 32

df = pd.read_json(INPUT_PATH, lines=True)

df["Publishdate"] = pd.to_datetime(df["Publishdate"], errors="coerce")

df = df.dropna(subset=["Publishdate", "Title", "Text"])

texts = (df["Title"] + ". " + df["Text"]).tolist()

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

scores = []

for i in range(0, len(texts), BATCH_SIZE):

    batch = texts[i:i + BATCH_SIZE]

    inputs = tokenizer(
        batch,
        padding=True,
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    positive = probabilities[:, 0]
    negative = probabilities[:, 1]

    batch_scores = positive - negative

    scores.extend(batch_scores.cpu().numpy())

    print(f"Processed {min(i + BATCH_SIZE, len(texts))}/{len(texts)}")

df["sentiment_score"] = scores

df[["Publishdate", "symbol", "Title", "sentiment_score"]].to_csv(
    OUTPUT_PATH,
    index=False
)

print("\nS&P 500 sentiment processing complete.")
print(f"Saved to: {OUTPUT_PATH}")