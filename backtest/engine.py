
from backtest.portfolio import Portfolio
from backtest.execution import ExecutionSimulator
from backtest.equity import EquityPoint

from signals.signal import Action


class BacktestEngine:

    def __init__(

        self,

        strategy,

        initial_cash=10000,

        quantity=1

    ):

        self.strategy = strategy

        self.portfolio = Portfolio(initial_cash)

        self.execution = ExecutionSimulator(

            self.portfolio

        )

        self.quantity = quantity

        self.equity_curve = []

    def run(self, df):

        symbol = df.iloc[0]["symbol"]

        #
        # Replay history candle by candle
        #

        for i in range(50, len(df)):

            history = df.iloc[: i + 1]

            current = history.iloc[-1]

            timestamp = current["timestamp"]

            price = float(current["close"])

            #
            # Ask strategy
            #

            signal = self.strategy.evaluate(

                history

            )

            #
            # BUY
            #

            if signal.action == Action.BUY:

                if not self.portfolio.has_position(

                    symbol

                ):

                    self.execution.execute_buy(

                        symbol=symbol,

                        price=price,

                        quantity=self.quantity,

                        timestamp=timestamp

                    )

            #
            # SELL
            #

            elif signal.action == Action.SELL:

                if self.portfolio.has_position(

                    symbol

                ):

                    self.execution.execute_sell(

                        symbol=symbol,

                        price=price,

                        timestamp=timestamp

                    )

            #
            # Record equity
            #

            equity = self.portfolio.update(
                {symbol: price}
            )

            self.equity_curve.append(

                EquityPoint(

                    timestamp=timestamp,

                    equity=equity

                )

            )

        #
        # Close any open trade
        #

        if self.portfolio.has_position(symbol):

            last = df.iloc[-1]

            self.execution.execute_sell(

                symbol=symbol,

                price=float(last["close"]),

                timestamp=last["timestamp"]

            )

        return self.portfolio.trade_history

