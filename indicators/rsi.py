import pandas as pd

from ta.momentum import RSIIndicator

from .base import Indicator


class RSI(Indicator):

    def __init__(self, period: int):

        self.period = period

    def apply(self, df):

        column = f"RSI_{self.period}"

        df[column] = RSIIndicator(
            close=df["close"],
            window=self.period
        ).rsi()

        return df
