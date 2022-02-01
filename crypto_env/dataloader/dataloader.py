from abc import ABC, abstractmethod


class DataLoader(ABC):
    @abstractmethod
    def __init__(self):
        super(DataLoader, self).__init__()

    @abstractmethod
    def get(self, index):
        raise NotImplementedError()

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError()
