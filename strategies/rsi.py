from strategies.base import Strategy
from signals.signal import Signal, Action


class RSIStrategy(Strategy):

    def evaluate(self, df):

        period = self.params.get("period", 14)
        oversold = self.params.get("oversold", 30)
        overbought = self.params.get("overbought", 70)

        last = df.iloc[-1]

        rsi = last[f"RSI_{period}"]

        if rsi <= oversold:

            return Signal(
                action=Action.BUY,
                symbol=last["symbol"],
                price=float(last["close"]),
                reason=f"RSI {rsi:.2f} <= {oversold}"
            )

        if rsi >= overbought:

            return Signal(
                action=Action.SELL,
                symbol=last["symbol"],
                price=float(last["close"]),
                reason=f"RSI {rsi:.2f} >= {overbought}"
            )

        return Signal(
            action=Action.HOLD,
            symbol=last["symbol"],
            price=float(last["close"]),
            reason=f"RSI {rsi:.2f}"
        )