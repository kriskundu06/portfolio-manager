from fastapi import APIRouter
import pandas as pd
import numpy as np

router = APIRouter()

BACKTEST_PATH = "data/processed/ppo_test.csv"


@router.get("/performance")
def get_performance():

    df = pd.read_csv(
        BACKTEST_PATH,
        parse_dates=["Date"]
    )

    return {
        "dates": df["Date"].dt.strftime("%Y-%m-%d").tolist(),
        "portfolio_value": df["Cumulative_Value"].tolist(),
        "returns": df["Portfolio_Return"].tolist(),
        "drawdown": (
            df["Cumulative_Value"]
            / df["Cumulative_Value"].cummax()
            - 1
        ).tolist()
    }


@router.get("/metrics")
def get_metrics():

    df = pd.read_csv(
        BACKTEST_PATH,
        parse_dates=["Date"]
    )

    returns = df["Portfolio_Return"].dropna()

    # CAGR
    start_value = df["Cumulative_Value"].iloc[0]
    end_value = df["Cumulative_Value"].iloc[-1]

    years = (
        df["Date"].iloc[-1] - df["Date"].iloc[0]
    ).days / 365.25

    cagr = (end_value / start_value) ** (1 / years) - 1

    # Sharpe Ratio
    sharpe = (
        returns.mean() / returns.std()
    ) * np.sqrt(12)

    # Sortino Ratio
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

    return {
        "cagr": float(cagr),
        "sharpe": float(sharpe),
        "sortino": float(sortino),
        "max_drawdown": float(max_drawdown)
    }