from .ema import EMA


class IndicatorEngine:

    def __init__(self):
        pass

    def add_ema(self, df, period):

        ema = EMA(period)

        return ema.apply(df)
