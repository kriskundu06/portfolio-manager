import pandas as pd
import numpy as np
DATA_PATH = "data/processed/monthly_features.csv"
def calculate_metrics(returns):

    total_return = (
        (1 + returns).prod() - 1
    )

    years = len(returns) / 12

    cagr = (
        (1 + total_return) ** (1 / years)
        - 1
    )

    volatility = (
        returns.std() * np.sqrt(12)
    )

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
    ) - 1

    max_drawdown = drawdown.min()

    calmar = (
        cagr / abs(max_drawdown)
    )

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Volatility": volatility,
        "Sharpe": sharpe,
        "Sortino": sortino,
        "Max Drawdown": max_drawdown,
        "Calmar": calmar
    }


df = pd.read_csv(
    DATA_PATH,
    parse_dates=["Date"]
)

df.set_index("Date", inplace=True)

df = df.loc[
    "2023-01-01":"2025-12-31"
]


# Equal-weight portfolio

equal_weight_returns = df[
    [
        "SP500_return_1m",
        "NASDAQ_return_1m",
        "GOLD_return_1m",
        "OIL_return_1m",
        "NIFTY_return_1m"
    ]
].mean(axis=1)


# S&P 500

sp500_returns = df[
    "SP500_return_1m"
]


equal_metrics = calculate_metrics(
    equal_weight_returns
)

sp500_metrics = calculate_metrics(
    sp500_returns
)


print("\n========== EQUAL WEIGHT ==========")

for metric, value in equal_metrics.items():
    print(f"{metric}: {value:.4f}")


print("\n========== S&P 500 ==========")
for metric, value in sp500_metrics.items():
    print(f"{metric}: {value:.4f}")