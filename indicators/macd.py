from ta.trend import MACD

from .base import Indicator


class MACDIndicator(Indicator):

    def __init__(
        self,
        fast=12,
        slow=26,
        signal=9
    ):

        self.fast = fast
        self.slow = slow
        self.signal = signal

    def apply(self, df):

        macd = MACD(
            close=df["close"],
            window_fast=self.fast,
            window_slow=self.slow,
            window_sign=self.signal
        )

        df["MACD"] = macd.macd()

        df["MACD_SIGNAL"] = macd.macd_signal()

        df["MACD_HIST"] = macd.macd_diff()

        return df
