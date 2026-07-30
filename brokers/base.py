from abc import ABC, abstractmethod


class Broker(ABC):

    @abstractmethod
    def connect(self):
        """Connect to broker"""
        pass

    @abstractmethod
    def account(self):
        """Return account information"""
        pass

    @abstractmethod
    def positions(self):
        """Return current positions"""
        pass

    @abstractmethod
    def bars(self, symbol: str, timeframe: str, limit: int = 100):
        """Return historical bars"""
        pass

    @abstractmethod
    def latest_price(self, symbol: str):
        """Return latest market price"""
        pass

    @abstractmethod
    def buy(self, symbol: str, qty: float):
        """Submit market buy order"""
        pass

    @abstractmethod
    def sell(self, symbol: str, qty: float):
        """Submit market sell order"""
        pass

    @abstractmethod
    def close(self, symbol: str):
        """Close an open position"""
        pass
