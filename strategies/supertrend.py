from strategies.base import Strategy
from signals.signal import Signal, Action



class SuperTrendStrategy(Strategy):

    def __init__(self,**kwargs):
        pass

    def evaluate(self, df):

        last = df.iloc[-1]

        symbol = last["symbol"]
        price = float(last["close"])

        if last["SUPERTREND_UP"]:

            return Signal(
                Action.BUY,
                symbol,
                price,
                "SuperTrend bullish"
            )

        return Signal(
            Action.SELL,
            symbol,
            price,
            "SuperTrend bearish"
        )