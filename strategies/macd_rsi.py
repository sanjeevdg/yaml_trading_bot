from strategies.base import Strategy
from signals.signal import Signal, Action


class MACDRSIStrategy(Strategy):

    def __init__(self, oversold=35, overbought=65):

        self.oversold = oversold
        self.overbought = overbought

    def evaluate(self, df):

        last = df.iloc[-1]

        close = float(last["close"])

        macd = float(last["MACD"])

        signal = float(last["MACD_SIGNAL"])

        rsi = float(last["RSI_14"])

        symbol = last["symbol"]

        if macd > signal and rsi < self.oversold:

            return Signal(
                Action.BUY,
                symbol,
                close,
                "Bullish MACD with oversold RSI"
            )

        if macd < signal and rsi > self.overbought:

            return Signal(
                Action.SELL,
                symbol,
                close,
                "Bearish MACD with overbought RSI"
            )

        return Signal(
            Action.HOLD,
            symbol,
            close,
            "No MACD/RSI setup"
        )