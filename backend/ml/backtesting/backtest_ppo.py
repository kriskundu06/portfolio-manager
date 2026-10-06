from stable_baselines3 import PPO
from backend.ml.environment.portfolio_env import PortfolioEnv
from pathlib import Path
import pandas as pd
MODEL_PATH = "models/ppo_market_baseline"

def run_backtest(start_date, end_date, output_file):
    env = PortfolioEnv(
        start_date=start_date,
        end_date=end_date
    )
    model = PPO.load(MODEL_PATH)
    observation, info = env.reset()
    results = []
    done = False
    while not done:
        action, _ = model.predict(
            observation,
            deterministic=True
        )
        observation, reward, terminated, truncated, info = env.step(
            action
        )
        results.append({
            "Date": info["date"],
            "Portfolio_Return": info["portfolio_return"],
            "Reward": reward,
            "Transaction_Cost": info["transaction_cost"],
            "Turnover": info["turnover"],
            "SP500_Weight": info["weights"][0],
            "NASDAQ_Weight": info["weights"][1],
            "GOLD_Weight": info["weights"][2],
            "OIL_Weight": info["weights"][3],
            "NIFTY_Weight": info["weights"][4]
        })

        done = terminated or truncated

    results = pd.DataFrame(results)

    results["Cumulative_Value"] = (
        1 + results["Portfolio_Return"]
    ).cumprod()

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    results.to_csv(
        output_path,
        index=False
    )

    print("\nBacktest complete.")
    print("Period:", start_date, "to", end_date)
    print("Months:", len(results))
    print("Saved to:", output_path)

    print("\nFinal portfolio value:")
    print(results["Cumulative_Value"].iloc[-1])


if __name__ == "__main__":

    run_backtest(
        start_date="2021-01-01",
        end_date="2022-12-31",
        output_file="data/processed/ppo_validation.csv"
    )

    run_backtest(
        start_date="2023-01-01",
        end_date="2025-12-31",
        output_file="data/processed/ppo_test.csv"
    )