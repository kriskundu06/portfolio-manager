from portfolio_env import PortfolioEnv
import numpy as np
env = PortfolioEnv()
observation, info = env.reset()
print("Initial observation shape:", observation.shape)
print("Initial weights:", env.weights)
print("Sum of weights:", np.sum(env.weights))

for step in range(5):

    action = np.random.randn(5)
    observation, reward, terminated, truncated, info = env.step(action)

    print("\nStep:", step + 1)
    print("Current date:", env.data.index[env.current_step])
    print("Observation shape:", observation.shape)
    print("Reward:", reward)
    print("Weights:", info["weights"])
    print("Weight sum:", np.sum(info["weights"]))
    print("Portfolio return:", info["portfolio_return"])
    print("Transaction cost:", info["transaction_cost"])
    print("Turnover:", info["turnover"])

    if terminated or truncated:
        break