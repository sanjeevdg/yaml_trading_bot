from strategies.base import Strategy
from signals.signal import Signal, Action


class EMARSIStrategy(Strategy):

    def evaluate(self, df):

        ema_period = self.params.get("ema", 20)
        rsi_period = self.params.get("period", 14)
        oversold = self.params.get("oversold", 35)
        overbought = self.params.get("overbought", 65)

        last = df.iloc[-1]

        ema = float(last[f"EMA_{ema_period}"])
        rsi = float(last[f"RSI_{rsi_period}"])
        close = float(last["close"])
        symbol = last["symbol"]

        #
        # Buy
        #

        if close > ema and rsi <= oversold:

            return Signal(
                action=Action.BUY,
                symbol=symbol,
                price=close,
                reason=f"Price > EMA{ema_period} and RSI {rsi:.2f} <= {oversold}"
            )

        #
        # Sell
        #

        if close < ema and rsi >= overbought:

            return Signal(
                action=Action.SELL,
                symbol=symbol,
                price=close,
                reason=f"Price < EMA{ema_period} and RSI {rsi:.2f} >= {overbought}"
            )

        #
        # Hold
        #

        return Signal(
            action=Action.HOLD,
            symbol=symbol,
            price=close,
            reason="EMA/RSI conditions not met"
        )