from strategies.base import Strategy
from signals.signal import Signal, Action


class SuperTrendStrategy(Strategy):

    def evaluate(self, df):

        period = self.params.get("period", 10)
        multiplier = self.params.get("multiplier", 3)

        last = df.iloc[-1]

        close = float(last["close"])
        supertrend = float(last["SUPERTREND"])

        symbol = last["symbol"]

        #
        # BUY
        #

        if close > supertrend:

            return Signal(
                action=Action.BUY,
                symbol=symbol,
                price=close,
                reason=f"Price above SuperTrend ({period}, {multiplier})"
            )

        #
        # SELL
        #

        if close < supertrend:

            return Signal(
                action=Action.SELL,
                symbol=symbol,
                price=close,
                reason=f"Price below SuperTrend ({period}, {multiplier})"
            )

        #
        # HOLD
        #

        return Signal(
            action=Action.HOLD,
            symbol=symbol,
            price=close,
            reason="Price on SuperTrend"
        )