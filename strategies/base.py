from abc import ABC, abstractmethod


class Strategy(ABC):

    def __init__(self, **kwargs):
        self.params = kwargs

    @abstractmethod
    def evaluate(self, df):
        pass