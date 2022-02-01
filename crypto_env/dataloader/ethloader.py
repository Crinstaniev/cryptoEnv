import os
import requests
import pandas as pd

from .dataloader import DataLoader


class ETHLoader(DataLoader):

    def __init__(self, base_dir, features: list,
                 url="https://raw.githubusercontent.com/coinmetrics/data/master/csv/eth.csv"):
        self.dir = os.path.join(base_dir, 'eth_data')
        self.data = pd.read_csv(url)[['time', *features]]

        if not os.path.isdir(self.dir):
            os.mkdir(self.dir)
        self.data.to_csv(os.path.join(self.dir, 'data.csv'))

    def __iter__(self):
        pass

    def get(self, index):
        pass
