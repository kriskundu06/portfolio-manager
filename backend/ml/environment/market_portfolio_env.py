import gymnasium as gym
from gymnasium import spaces
import pandas as pd
import numpy as np
from pathlib import Path

FEATURES_PATH = Path("data/processed/monthly_features.csv")

ASSETS = ["SP500", "NASDAQ", "GOLD", "OIL", "NIFTY"]

RETURN_COLUMNS = [
    f"{asset}_return_1m"
    for asset in ASSETS
]


class MarketPortfolioEnv(gym.Env):

    def __init__(
        self,
        start_date=None,
        end_date=None,
        transaction_cost=0.001
    ):
        super().__init__()

        self.transaction_cost = transaction_cost

        # The month is stored as the CSV index
        self.data = pd.read_csv(
            FEATURES_PATH,
            index_col=0
        )

        self.data.index = pd.to_datetime(
            self.data.index
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
            self.data.columns
        ]

        self.return_data = self.data[
            RETURN_COLUMNS
        ]

        self.n_assets = len(ASSETS)
        self.n_features = len(self.feature_data.columns)

        self.observation_space = spaces.Box(
            low=-np.inf,
            high=np.inf,
            shape=(self.n_features + self.n_assets,),
            dtype=np.float32
        )

        self.action_space = spaces.Box(
            low=-1,
            high=1,
            shape=(self.n_assets,),
            dtype=np.float32
        )

        self.current_step = 0

        self.weights = (
            np.ones(self.n_assets) / self.n_assets
        )

    def reset(self, seed=None, options=None):

        super().reset(seed=seed)

        self.current_step = 0

        self.weights = (
            np.ones(self.n_assets) / self.n_assets
        )

        observation = self._get_observation()

        return observation, {}

    def _get_observation(self):

        market_features = (
            self.feature_data.iloc[
                self.current_step
            ].values
        )

        observation = np.concatenate(
            [market_features, self.weights]
        )

        return observation.astype(np.float32)

    def _softmax(self, action):

        action = action - np.max(action)

        exp_action = np.exp(action)

        weights = exp_action / np.sum(exp_action)

        return weights