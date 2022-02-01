from abc import ABC, abstractmethod


class DataLoader(ABC):
    features: list
    _idx: int

    @abstractmethod
    def __init__(self):
        super(DataLoader, self).__init__()

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

    @property
    def idx(self):
        return self._idx
