from abc import ABC, abstractmethod

import pandas as pd


class MarketDataProvider(ABC):

    @abstractmethod
    def get_bars(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 200
    ) -> pd.DataFrame:
        """
        Return OHLCV data as a pandas DataFrame.
        """
        pass

    @abstractmethod
    def get_latest_price(
        self,
        symbol: str
    ) -> float:
        """
        Return the latest trade price.
        """
        pass
