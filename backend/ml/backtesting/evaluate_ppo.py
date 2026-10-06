import pandas as pd
import numpy as np
def calculate_metrics(file_path):
    df = pd.read_csv(file_path, parse_dates=["Date"])
    returns = df["Portfolio_Return"]
    total_return = (
        (1 + returns).prod() - 1
    )
    years = len(returns) / 12
    cagr = (
        (1 + total_return) ** (1 / years)
        - 1
    )
    volatility = returns.std() * np.sqrt(12)
    sharpe = (
        returns.mean() / returns.std()
    ) * np.sqrt(12)
    downside = returns[returns < 0]
    downside_deviation = (
        downside.std() * np.sqrt(12)
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
    ) -1
    max_drawdown = drawdown.min()
    calmar = cagr / abs(max_drawdown)
    average_turnover = df["Turnover"].mean()
    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_drawdown,
        "Calmar": calmar,
        "Average Turnover": average_turnover
    }
if __name__ == "__main__":
    validation = calculate_metrics(
        "data/processed/ppo_validation.csv"
    )
    test = calculate_metrics(
        "data/processed/ppo_test.csv"
    )
    print("\n========== VALIDATION 2021-2022 ==========")
    for metric, value in validation.items():
        print(f"{metric}: {value:.4f}")
    print("\n========== TEST 2023-2025 ==========")
    for metric, value in test.items():
        print(f"{metric}: {value:.4f}")
