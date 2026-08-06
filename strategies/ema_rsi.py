from strategies.base import Strategy
from signals.signal import Signal, Action


class EMARSIStrategy(Strategy):

    def __init__(
        self,
        ema=20,
        oversold=35,
        overbought=65
    ):
        self.ema = ema
        self.oversold = oversold
        self.overbought = overbought

    def evaluate(self, df):

        last = df.iloc[-1]

        ema = last[f"EMA_{self.ema}"]
        rsi = last["RSI_14"]
        close = float(last["close"])

        #
        # Buy
        #
        if close > ema and rsi < self.oversold:

            return Signal(
                action=Action.BUY,
                symbol=last["symbol"],
                price=close,
                reason="Above EMA and RSI oversold"
            )

        #
        # Sell
        #
        if close < ema and rsi > self.overbought:

            return Signal(
                action=Action.SELL,
                symbol=last["symbol"],
                price=close,
                reason="Below EMA and RSI overbought"
            )

        return Signal(
            action=Action.HOLD,
            symbol=last["symbol"],
            price=close,
            reason=(
                f"Close={close:.2f}, "
                f"EMA20={ema:.2f}, "
                f"RSI14={rsi:.1f}. "
                "Buy/Sell conditions not met."
            )
        )