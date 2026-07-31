from .base import Indicator


class IndicatorEngine:

    def __init__(self):

        self.indicators = []

    def add(self, indicator: Indicator):

        self.indicators.append(indicator)

    def apply(self, df):

        for indicator in self.indicators:

            df = indicator.apply(df)

        return df
