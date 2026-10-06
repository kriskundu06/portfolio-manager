import pandas as pd
import numpy as np
from pathlib import Path
RETURNS_PATH = Path("data/processed/daily_returns.csv")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
def create_monthly_features():
    print("Loading daily returns data..")
    returns = pd.read_csv(
        RETURNS_PATH,
        index_col="Date",
        parse_dates=True
    )
    print("Daily returns data loaded.")
    print(f"Shape: {returns.shape}")
    common_start = returns.dropna().index[0]
    returns = returns.loc[common_start:]
    print(f"Common start date: {common_start}")
    print(f"New shape: {returns.shape}")
    monthly_return = (
        (1 + returns)
        .resample("ME")
        .prod()
        - 1
    )
    monthly_return_3m = (
        (1 + monthly_return)
        .rolling(3)
        .apply(np.prod, raw=True)
        - 1
    )
    monthly_volatility = returns.resample("ME").std()
    monthly_sharpe = pd.DataFrame(
        index=monthly_return.index
    )
    #sortino
    monthly_sortino = pd.DataFrame(
        index=monthly_return.index)
    monthly_mdd = pd.DataFrame(
        index=monthly_return.index)
    for asset in returns.columns:
        asset_returns = returns[asset].dropna()
        rolling_mean = asset_returns.rolling(63).mean()
        rolling_std = asset_returns.rolling(63).std()
        sharpe = rolling_mean / rolling_std
        monthly_sharpe[f"{asset}_sharpe"] = (
            sharpe.resample("ME").last()
        )
        # Sortino
        downside_returns = asset_returns.where(
            asset_returns < 0,
            0
        )
        downside_deviation = (
            downside_returns
            .rolling(63)
            .apply(
                lambda x: np.sqrt(np.mean(x ** 2)),
                raw=True
            )
        )
        sortino = rolling_mean / downside_deviation
        monthly_sortino[f"{asset}_sortino"] = (
            sortino.resample("ME").last()
        )
        wealth = (1 + asset_returns).cumprod()
        rolling_peak = wealth.rolling(63).max()
        drawdown = (wealth / rolling_peak) - 1
        mdd = drawdown.resample("ME").min()
        monthly_mdd[f"{asset}_mdd"] = mdd
    correlation_features = pd.DataFrame(
        index=monthly_return.index
    )
    assets = returns.columns.tolist()
    for i in range(len(assets)):
        for j in range(i + 1, len(assets)):
            asset_1 = assets[i]
            asset_2 = assets[j]
            correlation_name = (
                f"{asset_1}_{asset_2}_corr"
            )
            asset_1_returns = returns[asset_1].dropna()
            asset_2_returns = returns[asset_2].dropna()
            pair = pd.concat(
                [
                    asset_1_returns,
                    asset_2_returns
                ],
                axis=1,
                join="inner"
            )
            pair.columns = [
                asset_1,
                asset_2
            ]
            pair_corr = (
                pair[asset_1]
                .rolling(63)
                .corr(pair[asset_2])
            )
            correlation_features[correlation_name] = (
                pair_corr.resample("ME").last()
            )
    monthly_return.columns = [
        f"{col}_return_1m"
        for col in monthly_return.columns
    ]
    monthly_return_3m.columns = [
        f"{col}_return_3m"
        for col in monthly_return_3m.columns
    ]
    monthly_volatility.columns = [
        f"{col}_volatility"
        for col in monthly_volatility.columns
    ]
    features = pd.concat(
        [
            monthly_return,
            monthly_return_3m,
            monthly_volatility,
            monthly_sharpe,
            monthly_sortino,
            monthly_mdd,
            correlation_features
        ],
        axis=1
    )
    features = features.dropna()
    output_path = OUTPUT_DIR / "monthly_features.csv"
    features.to_csv(output_path)
    print("\nMonthly features calculated.")
    print("\nSaved to:", output_path)
    print("\nNumber of features:")
    print(len(features.columns))
    print("\nFeatures:")
    print(features.columns.tolist())
    print("\nShape:")
    print(features.shape)
    print("\nFirst 5 rows of features:")
    print(features.head())
    print("\nLast 5 rows of features:")
    print(features.tail())
if __name__ == "__main__":
    create_monthly_features()