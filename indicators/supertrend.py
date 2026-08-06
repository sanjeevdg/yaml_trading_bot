import pandas as pd

from ta.volatility import AverageTrueRange

from .base import Indicator


class SuperTrend(Indicator):

    def __init__(self,
                 period=10,
                 multiplier=3):

        self.period = period
        self.multiplier = multiplier

    def apply(self, df):

        atr = AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=df["close"],
            window=self.period
        ).average_true_range()

        hl2 = (df["high"] + df["low"]) / 2

        upper = hl2 + self.multiplier * atr
        lower = hl2 - self.multiplier * atr

        st = [0.0] * len(df)
        direction = [True] * len(df)

        st[0] = lower.iloc[0]

        for i in range(1, len(df)):

            if df["close"].iloc[i] > upper.iloc[i - 1]:
                direction[i] = True

            elif df["close"].iloc[i] < lower.iloc[i - 1]:
                direction[i] = False

            else:
                direction[i] = direction[i - 1]

                if direction[i]:
                    lower.iloc[i] = max(
                        lower.iloc[i],
                        lower.iloc[i - 1]
                    )

                else:
                    upper.iloc[i] = min(
                        upper.iloc[i],
                        upper.iloc[i - 1]
                    )

            st[i] = lower.iloc[i] if direction[i] else upper.iloc[i]

        df["SUPERTREND"] = st
        df["SUPERTREND_UP"] = direction

        return df