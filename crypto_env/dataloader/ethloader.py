import os
import pandas as pd

from .dataloader import DataLoader


class ETHLoader(DataLoader):

    def __init__(self, base_dir, features: list,
                 url="https://raw.githubusercontent.com/coinmetrics/data/master/csv/eth.csv"):
        self.dir = os.path.join(base_dir, 'eth_data')
        self.features = features
        self.data = pd.read_csv(url)[[*features]]

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        self.data.to_csv(os.path.join(self.dir, 'data.csv'))
        # var for the iterator
        self._idx = 0

    def __len__(self):
        return len(self.data)

    def __next__(self):
        # end of the iteration
        if self._idx == len(self.data):
            raise StopIteration()

        payload = self.data.iloc[self._idx]
        self._idx += 1
        return self._idx - 1, payload

    def reset(self):
        self._idx = 0
