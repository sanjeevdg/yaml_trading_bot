from strategies.base import Strategy
from signals.signal import Signal, Action


class RSIStrategy(Strategy):

    def __init__(self,
                 period=14,
                 oversold=30,
                 overbought=70):

        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def evaluate(self, df):

        last = df.iloc[-1]

        rsi = last[f"RSI_{self.period}"]

        if rsi <= self.oversold:

            return Signal(
                action=Action.BUY,
                symbol=last["symbol"],
                price=float(last["close"]),
                reason=f"RSI {rsi:.2f} <= {self.oversold}"
            )

        if rsi >= self.overbought:

            return Signal(
                action=Action.SELL,
                symbol=last["symbol"],
                price=float(last["close"]),
                reason=f"RSI {rsi:.2f} >= {self.overbought}"
            )

        return Signal(
            action=Action.HOLD,
            symbol=last["symbol"],
            price=float(last["close"]),
            reason=f"RSI {rsi:.2f}"
        )
