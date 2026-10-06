from fastapi import APIRouter
from stable_baselines3 import PPO
from backend.ml.environment.market_portfolio_env import MarketPortfolioEnv

router = APIRouter()

MODEL_PATH = "models/ppo_market_baseline"


@router.get("/portfolio")
def get_portfolio():

    env = MarketPortfolioEnv(
        start_date="2023-01-01",
        end_date="2025-12-31"
    )

    model = PPO.load(MODEL_PATH)

    observation, _ = env.reset()

    action, _ = model.predict(
        observation,
        deterministic=True
    )

    weights = env._softmax(action)

    return {
        "SP500": float(weights[0]),
        "NASDAQ": float(weights[1]),
        "GOLD": float(weights[2]),
        "OIL": float(weights[3]),
        "NIFTY": float(weights[4])
    }