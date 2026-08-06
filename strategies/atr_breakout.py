from strategies.base import Strategy
from signals.signal import Signal, Action


class ATRBreakoutStrategy(Strategy):

    def __init__(self, period=14, multiplier=2):

        self.period = period
        self.multiplier = multiplier

    def evaluate(self, df):

        last = df.iloc[-1]
        prev = df.iloc[-2]

        close = float(last["close"])
        atr = float(last["ATR"])

        upper = prev["high"] + atr * self.multiplier
        lower = prev["low"] - atr * self.multiplier

        symbol = last["symbol"]

        if close > upper:

            return Signal(
                Action.BUY,
                symbol,
                close,
                f"ATR breakout above {upper:.2f}"
            )

        if close < lower:

            return Signal(
                Action.SELL,
                symbol,
                close,
                f"ATR breakdown below {lower:.2f}"
            )

        return Signal(
            Action.HOLD,
            symbol,
            close,
            "No ATR breakout"
        )