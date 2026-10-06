import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np
from pathlib import Path


FEATURES_PATH = Path(
    "data/processed/monthly_features_sentiment_v2.csv"
)

ASSETS = [
    "SP500",
    "NASDAQ",
    "GOLD",
    "OIL",
    "NIFTY"
]

RETURN_COLUMNS = [
    f"{asset}_return_1m"
    for asset in ASSETS
]

FEATURE_COLUMNS = [
    col for col in pd.read_csv(
        FEATURES_PATH,
        nrows=1
    ).columns
    if col != "month"
]


class PortfolioEnv(gym.Env):

    def __init__(
        self,
        start_date=None,
        end_date=None,
        transaction_cost=0.001
    ):

        super().__init__()

        self.transaction_cost = transaction_cost

        self.data = pd.read_csv(FEATURES_PATH)

        self.data["month"] = pd.to_datetime(
            self.data["month"]
        )

        self.data.set_index(
            "month",
            inplace=True
        )

        if start_date is not None:
            self.data = self.data[
                self.data.index >= start_date
            ]

        if end_date is not None:
            self.data = self.data[
                self.data.index <= end_date
            ]

        self.feature_data = self.data[
            FEATURE_COLUMNS
        ]

        self.return_data = self.data[
            RETURN_COLUMNS
        ]

        self.n_assets = len(ASSETS)

        self.n_features = len(
            FEATURE_COLUMNS
        )

        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(
                self.n_features + self.n_assets,
            ),
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=-1,
            high=1,
            shape=(self.n_assets,),
            dtype=np.float32
        )

        self.current_step = 0

        self.weights = np.ones(
            self.n_assets
        ) / self.n_assets


    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        self.current_step = 0

        self.weights = np.ones(
            self.n_assets
        ) / self.n_assets

        observation = self._get_observation()

        return observation, {}


    def _get_observation(self):

        market_features = self.feature_data.iloc[
            self.current_step
        ].values

        observation = np.concatenate(
            [
                market_features,
                self.weights
            ]
        )

        return observation.astype(
            np.float32
        )


    def _softmax(self, action):

        action = action - np.max(action)

        exp_action = np.exp(action)

        weights = (
            exp_action /
            np.sum(exp_action)
        )

        return weights


    def step(self, action):

        new_weights = self._softmax(
            action
        )

        old_weights = self.weights.copy()

        turnover = np.sum(
            np.abs(
                new_weights - old_weights
            )
        )

        transaction_cost = (
            self.transaction_cost *
            turnover
        )

        next_step = (
            self.current_step + 1
        )

        if next_step >= len(self.data):

            return (
                self._get_observation(),
                0.0,
                True,
                False,
                {}
            )

        next_returns = self.return_data.iloc[
            next_step
        ].values

        portfolio_return = np.sum(
            new_weights * next_returns
        )

        reward = (
            portfolio_return
            - transaction_cost
        )

        self.weights = new_weights

        self.current_step = next_step

        observation = self._get_observation()

        terminated = (
            self.current_step >=
            len(self.data) - 1
        )

        info = {
            "date": self.data.index[
                self.current_step
            ],
            "portfolio_return": portfolio_return,
            "transaction_cost": transaction_cost,
            "turnover": turnover,
            "weights": self.weights.copy()
        }

        return (
            observation,
            float(reward),
            terminated,
            False,
            info
        )