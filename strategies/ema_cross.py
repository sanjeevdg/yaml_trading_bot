from strategies.base import Strategy
from signals.signal import Signal, Action


class EMACrossStrategy(Strategy):

    
    def evaluate(self, df):

        fast_period = self.params.get("fast", 10)
        slow_period = self.params.get("slow", 20)

        previous = df.iloc[-2]
        current = df.iloc[-1]

        fast_col = f"EMA_{fast_period}"
        slow_col = f"EMA_{slow_period}"
        #
        # Bullish crossover
        #
        if (
            previous[fast_col] <= previous[slow_col]
            and current[fast_col] > current[slow_col]
        ):
            return Signal(
                action=Action.BUY,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason=f"EMA{fast_period} crossed above EMA{slow_period}"
            )

        if (
            previous[fast_col] >= previous[slow_col]
            and current[fast_col] < current[slow_col]
        ):
            return Signal(
                action=Action.SELL,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason=f"EMA{fast_period} crossed below EMA{slow_period}"
            )

        return Signal(
            action=Action.HOLD,
            symbol=current["symbol"],
            price=float(current["close"]),
            reason="No crossover"
        )
