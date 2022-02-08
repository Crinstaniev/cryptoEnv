from abc import ABC, abstractmethod


class DataLoader(ABC):
    _features: list
    _idx: int

    @abstractmethod
    def __init__(self, start_idx, end_idx):
        super(DataLoader, self).__init__()
        self._start_idx = start_idx,
        self._end_idx = end_idx

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        raise NotImplementedError()

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()

    @abstractmethod
    def get_feature(self, feature_name):
        raise NotImplementedError()

    @abstractmethod
    def get_duration(self):
        raise NotImplementedError()

    @property
    def idx(self):
        return self._idx
