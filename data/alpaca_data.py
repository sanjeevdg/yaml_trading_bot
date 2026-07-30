from datetime import datetime, timedelta

import pandas as pd

from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
#from alpaca.data.timeframe import TimeFrame
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from dotenv import load_dotenv

import os

from .base import MarketDataProvider

load_dotenv()


class AlpacaMarketData(MarketDataProvider):

    def __init__(self):

        self.client = StockHistoricalDataClient(
            os.getenv("ALPACA_API_KEY"),
            os.getenv("ALPACA_SECRET_KEY")
        )

    def _timeframe(self, tf: str):

        mapping = {
            "1Min": TimeFrame(1, TimeFrameUnit.Minute),
            "5Min": TimeFrame(5, TimeFrameUnit.Minute),
            "15Min": TimeFrame(15, TimeFrameUnit.Minute),
            "30Min": TimeFrame(30, TimeFrameUnit.Minute),
            "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
            "1Day": TimeFrame(1, TimeFrameUnit.Day),
        }

        if tf not in mapping:
            raise ValueError(f"Unsupported timeframe: {tf}")

        return mapping[tf]

    def get_bars(
        self,
        symbol,
        timeframe,
        limit=200
    ):

        request = StockBarsRequest(

            symbol_or_symbols=symbol,

            timeframe=self._timeframe(timeframe),

            start=datetime.utcnow() - timedelta(days=30),

            limit=limit

        )

        bars = self.client.get_stock_bars(request)

        df = bars.df.reset_index()

        return df

    def get_latest_price(self, symbol):

        df = self.get_bars(
            symbol,
            "1Min",
            1
        )

        return float(df.iloc[-1]["close"])
