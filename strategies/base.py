from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def evaluate(self, df):
        """
        Returns a Signal
        """
        pass
