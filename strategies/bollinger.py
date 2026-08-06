from strategies.base import Strategy
from signals.signal import Signal, Action


class BollingerStrategy(Strategy):


    def evaluate(self, df):

        period = self.params.get("period", 20)
        stddev = self.params.get("stddev", 2)

        last = df.iloc[-1]

        close = float(last["close"])

        upper = last["BB_UPPER"]

        lower = last["BB_LOWER"]

        symbol = last["symbol"]

        #
        # BUY
        #
        if close < lower:

            return Signal(
                action=Action.BUY,
                symbol=symbol,
                price=close,
                reason="Price below lower Bollinger Band"
            )

        #
        # SELL
        #
        if close > upper:

            return Signal(
                action=Action.SELL,
                symbol=symbol,
                price=close,
                reason="Price above upper Bollinger Band"
            )

        return Signal(
            action=Action.HOLD,
            symbol=symbol,
            price=close,
            reason="Inside Bollinger Bands"
        )