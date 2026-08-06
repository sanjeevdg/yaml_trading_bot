from strategies.base import Strategy
from signals.signal import Signal, Action


class EMAMACDStrategy(Strategy):

    def __init__(self, ema=20):
        self.ema = ema

    def evaluate(self, df):

        last = df.iloc[-1]

        close = float(last["close"])

        ema = float(last[f"EMA_{self.ema}"])

        macd = float(last["MACD"])

        signal = float(last["MACD_SIGNAL"])

        symbol = last["symbol"]

        if close > ema and macd > signal:

            return Signal(
                Action.BUY,
                symbol,
                close,
                "Price above EMA and MACD bullish"
            )

        if close < ema and macd < signal:

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