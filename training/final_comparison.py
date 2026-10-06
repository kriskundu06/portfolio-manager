import pandas as pd


FILES = {
    "Market PPO": "data/processed/ppo_test.csv",
    "Sentiment PPO v1": "data/processed/ppo_sentiment_test.csv",
    "Sentiment PPO v2": "data/processed/ppo_sentiment_v2_test.csv"
}


def calculate_metrics(file_path):

    df = pd.read_csv(
        file_path,
        parse_dates=["Date"]
    )

    returns = df["Portfolio_Return"]

    total_return = (
        (1 + returns).prod() - 1
    )

    years = len(returns) / 12

    cagr = (
        (1 + total_return) ** (1 / years)
        - 1
    )

    volatility = (
        returns.std() * (12 ** 0.5)
    )

    sharpe = (
        returns.mean() / returns.std()
    ) * (12 ** 0.5)

    downside = returns[returns < 0]

    downside_deviation = (
        downside.std() * (12 ** 0.5)
    )

    sortino = (
        returns.mean() * 12
    ) / downside_deviation

    cumulative = (
        1 + returns
    ).cumprod()

    peak = cumulative.cummax()

    drawdown = (
        cumulative / peak
    ) - 1

    max_drawdown = drawdown.min()

    calmar = (
        cagr / abs(max_drawdown)
    )

    turnover = df["Turnover"].mean()

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_drawdown,
        "Calmar": calmar,
        "Average Turnover": turnover
    }


results = {}

for model, file_path in FILES.items():

    results[model] = calculate_metrics(
        file_path
    )


comparison = pd.DataFrame(results).T

comparison.to_csv(
    "data/processed/final_model_comparison.csv"
)

print("\n========== FINAL MODEL COMPARISON ==========\n")

print(
    comparison.to_string(
        float_format=lambda x: f"{x:.4f}"
    )
)

print(
    "\nSaved to: "
    "data/processed/final_model_comparison.csv"
)