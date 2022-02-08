from gym.spaces import Box, Dict, Discrete
import gym
import numpy as np

from crypto_env.types import Transaction, create_info_type
from crypto_env.dataloader.dataloader import DataLoader
from crypto_env.recorder import Recorder


class CryptoEnv(gym.Env):

    def __init__(self, transaction_low, transaction_high, dataloader: DataLoader, recorder: Recorder):
        # transaction fees are not implemented in this environment. should be implemented in the algorithm (agent)
        super(CryptoEnv, self).__init__()

        assert (isinstance(dataloader, DataLoader))

        self.dataloader = dataloader
        self._len_data = len(dataloader)
        self._len_features = len(dataloader._features)
        self.Info = create_info_type(dataloader._features)
        self.recorder = recorder

        # define observation space: period market data. won't change due to action of the agent.
        self.observation_space = Dict({
            'index': Box(low=0, high=self._len_data - 1, shape=(1,), dtype=np.int32),
            'features': Box(low=-np.inf,
                            high=np.inf,
                            shape=(len(self.dataloader._features),)),
        })

        # define action space:
        # signal: 0: buy, 1: sell, 2: hold.
        self.action_space = Dict({
            'signal': Discrete(3),
            'value': Box(low=transaction_low, high=transaction_high, shape=(1,))
        })

    def step(self, action=None):
        # the history data will be returned as info from the recorder.
        signal = action['signal']
        value = action['value']
        transaction = Transaction(signal=signal, value=value[0])
        try:
            idx, info = next(self.dataloader)
        except StopIteration:
            idx = self.dataloader.idx + 1
            info = None
        observation = dict(
            features=np.array(list(info)),
            index=np.array([idx])
        )

        self.recorder.insert_transaction(transaction=transaction)
        self.recorder.insert_info(info=info)

        reward = 0.0  # reward is not implemented yet.
        info = dict()
        done = False
        if idx + 1 == len(self.dataloader):
            done = True

        return observation, reward, done, info

    def first_observation(self):
        self.reset()
        idx, info = next(self.dataloader)
        observation = dict(
            features=np.array(list(info)),
            index=np.array([0])
        )
        return observation

    def reset(self):
        self.dataloader.reset()
        self.recorder.reset()
        return self

    def render(self, mode="human"):
        pass

    def meta(self):
        # return meta information
        return dict(
            signals=dict(
                buy=0,
                sell=1,
                hold=2
            )
        )
