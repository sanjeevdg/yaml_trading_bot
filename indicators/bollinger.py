
from ta.volatility import BollingerBands

from indicators.base import Indicator


class Bollinger(Indicator):

    def __init__(self, period=20, stddev=2):

        self.period = period
        self.stddev = stddev

    def apply(self, df):

        bb = BollingerBands(

            close=df["close"],

            window=self.period,

            window_dev=self.stddev

        )

        df["BB_UPPER"] = bb.bollinger_hband()

        df["BB_MIDDLE"] = bb.bollinger_mavg()

        df["BB_LOWER"] = bb.bollinger_lband()

        df["BB_WIDTH"] = bb.bollinger_wband()

        return df