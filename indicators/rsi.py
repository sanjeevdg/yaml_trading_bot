from ta.momentum import RSIIndicator

from .base import Indicator


class RSI(Indicator):

    def __init__(self, period=14):

        self.period = period

    def apply(self, df):

        df[f"RSI_{self.period}"] = RSIIndicator(
            close=df["close"],
            window=self.period
        ).rsi()

        return df
