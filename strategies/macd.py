from strategies.base import Strategy
from signals.signal import Signal, Action


class MACDStrategy(Strategy):

    def evaluate(self, df):

        previous = df.iloc[-2]
        current = df.iloc[-1]

        #
        # Bullish crossover
        #
        if (
            previous["MACD"] <= previous["MACD_SIGNAL"]
            and current["MACD"] > current["MACD_SIGNAL"]
        ):

            return Signal(
                action=Action.BUY,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason="MACD crossed above Signal"
            )

        #
        # Bearish crossover
        #
        if (
            previous["MACD"] >= previous["MACD_SIGNAL"]
            and current["MACD"] < current["MACD_SIGNAL"]
        ):

            return Signal(
                action=Action.SELL,
                symbol=current["symbol"],
                price=float(current["close"]),
                reason="MACD crossed below Signal"
            )

        return Signal(
            action=Action.HOLD,
            symbol=current["symbol"],
            price=float(current["close"]),
            reason="No crossover"
        )
