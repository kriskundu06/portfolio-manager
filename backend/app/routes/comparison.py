from fastapi import APIRouter
import pandas as pd
import numpy as np

router = APIRouter(
    prefix="/comparison",
    tags=["Model Comparison"]
)


MODELS = [
    {
        "name": "Market PPO",
        "path": "data/processed/ppo_test.csv"
    },
    {
        "name": "Sentiment PPO v1",
        "path": "data/processed/ppo_sentiment_test.csv"
    },
    {
        "name": "Sentiment PPO v2",
        "path": "data/processed/ppo_sentiment_v2_test.csv"
    }
]


def calculate_metrics(path):

    df = pd.read_csv(
        path,
        parse_dates=["Date"]
    )

    returns = df["Portfolio_Return"].dropna()

    # Total Return
    total_return = (
        df["Cumulative_Value"].iloc[-1] - 1
    )

    # CAGR
    start_value = df["Cumulative_Value"].iloc[0]
    end_value = df["Cumulative_Value"].iloc[-1]

    years = (
        df["Date"].iloc[-1] - df["Date"].iloc[0]
    ).days / 365.25

    cagr = (
        end_value / start_value
    ) ** (1 / years) - 1

    # Volatility
    volatility = returns.std() * np.sqrt(12)

    # Sharpe
    sharpe = (
        returns.mean() / returns.std()
    ) * np.sqrt(12)

    # Sortino
    downside_returns = returns[returns < 0]

    downside_deviation = downside_returns.std()

    sortino = (
        returns.mean() / downside_deviation
    ) * np.sqrt(12)

    # Maximum Drawdown
    drawdown = (
        df["Cumulative_Value"]
        / df["Cumulative_Value"].cummax()
        - 1
    )

    max_drawdown = drawdown.min()

    # Calmar
    calmar = cagr / abs(max_drawdown)

    # Average Turnover
    average_turnover = df["Turnover"].mean()

    return {
        "total_return": float(total_return),
        "cagr": float(cagr),
        "volatility": float(volatility),
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "max_drawdown": float(max_drawdown),
        "calmar": float(calmar),
        "average_turnover": float(average_turnover)
    }


@router.get("")
def get_model_comparison():

    results = []

    for model in MODELS:

        metrics = calculate_metrics(
            model["path"]
        )

        results.append({
            "name": model["name"],
            **metrics
        })

    return {
        "models": results
    }   