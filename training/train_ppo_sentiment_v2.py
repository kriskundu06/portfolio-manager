from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from backend.ml.environment.portfolio_env import PortfolioEnv


train_env = PortfolioEnv(
    start_date="2008-01-01",
    end_date="2020-12-31"
)

check_env(
    train_env,
    warn=True
)

print(
    "Sentiment v2 environment is valid "
    "and ready for training."
)


model = PPO(
    policy="MlpPolicy",
    env=train_env,
    learning_rate=0.0003,
    n_steps=128,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    ent_coef=0.01,
    verbose=1
)


model.learn(
    total_timesteps=100000
)


model.save(
    "models/ppo_market_sentiment_v2"
)


print("\nSentiment PPO v2 training complete.")
print(
    "Model saved to "
    "models/ppo_market_sentiment_v2"
)