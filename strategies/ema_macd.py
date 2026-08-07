from strategies.base import Strategy
from signals.signal import Signal, Action


class EMAMACDStrategy(Strategy):

    def evaluate(self, df):

        ema_period = self.params.get("ema", 20)

        last = df.iloc[-1]

        close = float(last["close"])

        ema = float(last[f"EMA_{ema_period}"])

        macd = float(last["MACD"])

        macd_signal = float(last["MACD_SIGNAL"])

        symbol = last["symbol"]

        if close > ema and macd > macd_signal:

            return Signal(
                Action.BUY,
                symbol,
                close,
                "Price above EMA and MACD bullish"
            )

        if close < ema and macd < macd_signal:

            return Signal(
                Action.SELL,
                symbol,
                close,
                "Price below EMA and MACD bearish"
            )

        return Signal(
            Action.HOLD,
            symbol,
            close,
            "No EMA/MACD confirmation"
        )