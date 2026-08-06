
from ta.volatility import AverageTrueRange

from indicators.base import Indicator


class ATR(Indicator):

    def __init__(self, period=14):
        self.period = period

    def apply(self, df):

        atr = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=self.period
        )

        df["ATR"] = atr.average_true_range()

        return df