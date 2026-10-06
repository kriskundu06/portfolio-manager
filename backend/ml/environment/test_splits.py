from portfolio_env import PortfolioEnv


train_env = PortfolioEnv(
    start_date="2008-01-01",
    end_date="2020-12-31"
)

validation_env = PortfolioEnv(
    start_date="2021-01-01",
    end_date="2022-12-31"
)

test_env = PortfolioEnv(
    start_date="2023-01-01",
    end_date="2025-12-31"
)


print("TRAINING")
print("Start:", train_env.data.index[0])
print("End:", train_env.data.index[-1])
print("Months:", len(train_env.data))


print("\nVALIDATION")
print("Start:", validation_env.data.index[0])
print("End:", validation_env.data.index[-1])
print("Months:", len(validation_env.data))


print("\nTEST")
print("Start:", test_env.data.index[0])
print("End:", test_env.data.index[-1])
print("Months:", len(test_env.data))