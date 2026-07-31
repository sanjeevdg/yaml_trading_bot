from strategies.base import Strategy
from signals.signal import Signal, Action


class EMACrossStrategy(Strategy):

    def __init__(self, fast=10, slow=20):

        self.fast = fast
        self.slow = slow


    def evaluate(self, df):

        previous = df.iloc[-2]
        current = df.iloc[-1]
        fast = f"EMA_{self.fast}"
        slow = f"EMA_{self.slow}"
        #
        # Bullish crossover
        #
        if (
            previous["EMA_10"] <= previous["EMA_20"]
            and current["EMA_10"] > current["EMA_20"]
        ):

            return Signal(
                action=Action.BUY,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason="EMA10 crossed above EMA20"
            )

        #
        # Bearish crossover
        #
        if (
            previous["EMA_10"] >= previous["EMA_20"]
            and current["EMA_10"] < current["EMA_20"]
        ):

            return Signal(
                action=Action.SELL,
                symbol=current["symbol"],
                price=current["close"],
                reason="EMA10 crossed below EMA20"
            )

        #
        # No crossover
        #
        return Signal(
            action=Action.HOLD,
            symbol=current["symbol"],
            price=current["close"],
            reason="No crossover"
        )
