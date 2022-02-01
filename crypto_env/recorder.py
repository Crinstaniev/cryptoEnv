import pandas as pd
import numpy as np

from crypto_env.types import Transaction


class Recorder:
    def __init__(self) -> None:
        self.transaction_record = list()
        self.info_record = list()
        self.idx = 0
        self.indexes = None

    def insert_transaction(self, transaction):
        self.transaction_record.append(transaction)

    def insert_info(self, info):
        if self.indexes is None:
            self.indexes = info.index
        self.info_record.append(list(info))

    def get_transaction_record(self, to_dataframe=True):
        if to_dataframe:
            return pd.DataFrame(self.transaction_record)
        return self.transaction_record

    def get_info_record(self, to_dataframe=True):
        if to_dataframe:
            return pd.DataFrame(self.info_record, columns=self.indexes)
        return self.info_record
