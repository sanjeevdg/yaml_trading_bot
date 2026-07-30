import pandas as pd
from ta.trend import EMAIndicator

from .base import Indicator


class EMA(Indicator):

    def __init__(self, period: int):
        self.period = period

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:

        column = f"EMA_{self.period}"

        df[column] = EMAIndicator(
            close=df["close"],
            window=self.period
        ).ema_indicator()

        return df
