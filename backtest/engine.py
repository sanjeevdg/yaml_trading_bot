from rich import print

from .position import Position
from .trade import Trade


class BacktestEngine:

    def __init__(self, strategy):

        self.strategy = strategy

        self.position = None

        self.trades = []

    def run(self, df):

        #
        # Need enough candles for indicators
        #
        start = 50

        for i in range(start, len(df)):

            history = df.iloc[: i + 1]

            signal = self.strategy.evaluate(history)

            current = history.iloc[-1]

            price = float(current["close"])

            timestamp = current["timestamp"]

            symbol = current["symbol"]

            #
            # BUY
            #
            if signal.action.value == "BUY":

                if self.position is None:

                    self.position = Position(
                        symbol=symbol,
                        quantity=1,
                        entry_price=price,
                        entry_time=timestamp
                    )

                    print(
                        f"[green]BUY[/green] "
                        f"{symbol} @ {price:.2f}"
                    )

            #
            # SELL
            #
            elif signal.action.value == "SELL":

                if self.position is not None:

                    pnl = (
                        price
                        - self.position.entry_price
                    ) * self.position.quantity

                    trade = Trade(

                        symbol=symbol,

                        entry_time=self.position.entry_time,

                        exit_time=timestamp,

                        entry_price=self.position.entry_price,

                        exit_price=price,

                        quantity=self.position.quantity,

                        pnl=pnl

                    )

                    self.trades.append(trade)

                    print(
                        f"[red]SELL[/red] "
                        f"{symbol} "
                        f"P/L={pnl:.2f}"
                    )

                    self.position = None

        #
        # Close any open trade at the end
        #
        if self.position is not None:

            last = df.iloc[-1]

            pnl = (
                float(last["close"])
                - self.position.entry_price
            ) * self.position.quantity

            self.trades.append(

                Trade(

                    symbol=self.position.symbol,

                    entry_time=self.position.entry_time,

                    exit_time=last["timestamp"],

                    entry_price=self.position.entry_price,

                    exit_price=float(last["close"]),

                    quantity=self.position.quantity,

                    pnl=pnl

                )

            )

        return self.trades
