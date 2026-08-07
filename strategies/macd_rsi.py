from strategies.base import Strategy
from signals.signal import Signal, Action


class MACDRSIStrategy(Strategy):

    def evaluate(self, df):

        rsi_period = self.params.get("period", 14)
        oversold = self.params.get("oversold", 35)
        overbought = self.params.get("overbought", 65)

        last = df.iloc[-1]

        macd = float(last["MACD"])
        signal = float(last["MACD_SIGNAL"])
        rsi = float(last[f"RSI_{rsi_period}"])

        close = float(last["close"])
        symbol = last["symbol"]

        #
        # BUY
        #

        if macd > signal and rsi <= oversold:

            return Signal(
                action=Action.BUY,
                symbol=symbol,
                price=close,
                reason=f"MACD bullish and RSI {rsi:.2f} <= {oversold}"
            )

        #
        # SELL
        #

        if macd < signal and rsi >= overbought:

            return Signal(
                action=Action.SELL,
                symbol=symbol,
                price=close,
                reason=f"MACD bearish and RSI {rsi:.2f} >= {overbought}"
            )

        #
        # HOLD
        #

        return Signal(
            action=Action.HOLD,
            symbol=symbol,
            price=close,
            reason="MACD/RSI conditions not met"
        )