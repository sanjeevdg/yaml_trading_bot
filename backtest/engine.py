from backtest.portfolio import Portfolio
from backtest.execution import ExecutionSimulator
from backtest.equity import EquityPoint

from signals.signal import Action
from backtest.performance import PerformanceAnalyzer


class BacktestEngine:

    def __init__(
        self,
        strategy,
        initial_cash=10000,
        quantity=1,
        risk=None
    ):

        self.strategy = strategy

        self.portfolio = Portfolio(
            initial_cash
        )

        self.execution = ExecutionSimulator(
            self.portfolio
        )

        self.quantity = quantity

        self.risk = risk

        self.equity_curve = []

    # ---------------------------------------------------------
    # Risk configuration helper
    # ---------------------------------------------------------

    def get_risk_value(self, name):

        if self.risk is None:
            return None

        if isinstance(self.risk, dict):

            return self.risk.get(name)

        return getattr(
            self.risk,
            name,
            None
        )

    # ---------------------------------------------------------
    # Calculate stop-loss / take-profit
    # ---------------------------------------------------------

    def calculate_risk_levels(self, price):

        risk = self.cfg.risk.model_dump(
            exclude_none=True
        )

        stop_loss_percent = risk.get("stop_loss")
        take_profit_percent = risk.get("take_profit")

        entry_price = float(price)

        stop_loss = None
        take_profit = None

        if stop_loss_percent is not None:
            stop_loss = entry_price * (
                1 - float(stop_loss_percent) / 100
            )

        if take_profit_percent is not None:
            take_profit = entry_price * (
                1 + float(take_profit_percent) / 100
            )

        return stop_loss, take_profit

    # ---------------------------------------------------------
    # Run backtest
    # ---------------------------------------------------------

    def run(self, df):

        symbol = df.iloc[0]["symbol"]

        # -----------------------------------------------------
        # Replay history candle by candle
        # -----------------------------------------------------

        for i in range(50, len(df)):

            history = df.iloc[:i + 1]

            current = history.iloc[-1]

            timestamp = current["timestamp"]

            price = float(
                current["close"]
            )

            # -------------------------------------------------
            # Check existing position
            # for Stop Loss / Take Profit
            # -------------------------------------------------

            if self.portfolio.has_position(symbol):

                position = self.portfolio.positions[
                    symbol
                ]

                low = float(
                    current["low"]
                )

                high = float(
                    current["high"]
                )

                # -------------------------------------------------
                # Conservative assumption:
                #
                # If both SL and TP are reached during the
                # same candle, assume SL happened first.
                # -------------------------------------------------

                if (
                    position.stop_loss is not None
                    and low <= position.stop_loss
                ):

                    self.execution.execute_sell(

                        symbol=symbol,

                        price=position.stop_loss,

                        timestamp=timestamp,

                        exit_reason="STOP_LOSS"
                    )

                    continue

                if (
                    position.take_profit is not None
                    and high >= position.take_profit
                ):

                    self.execution.execute_sell(

                        symbol=symbol,

                        price=position.take_profit,

                        timestamp=timestamp,

                        exit_reason="TAKE_PROFIT"
                    )

                    continue

            # -------------------------------------------------
            # Ask strategy
            # -------------------------------------------------

            signal = self.strategy.evaluate(
                history
            )

            # -------------------------------------------------
            # BUY
            # -------------------------------------------------

            if signal.action == Action.BUY:

                if not self.portfolio.has_position(
                    symbol
                ):

                    stop_loss, take_profit = (
                        self.calculate_risk_levels(
                            price
                        )
                    )

                    self.execution.execute_buy(

                        symbol=symbol,

                        price=price,

                        quantity=self.quantity,

                        timestamp=timestamp,

                        stop_loss=stop_loss,

                        take_profit=take_profit
                    )

            # -------------------------------------------------
            # SELL
            # -------------------------------------------------

            elif signal.action == Action.SELL:

                if self.portfolio.has_position(
                    symbol
                ):

                    self.execution.execute_sell(

                        symbol=symbol,

                        price=price,

                        timestamp=timestamp,

                        exit_reason="STRATEGY"
                    )

            # -------------------------------------------------
            # Record equity
            # -------------------------------------------------

            equity = self.portfolio.update(
                {symbol: price}
            )

            self.equity_curve.append(

                EquityPoint(

                    timestamp=timestamp,

                    equity=equity

                )
            )

        # -----------------------------------------------------
        # Close any open trade at end of backtest
        # -----------------------------------------------------

        if self.portfolio.has_position(symbol):

            last = df.iloc[-1]

            self.execution.execute_sell(

                symbol=symbol,

                price=float(
                    last["close"]
                ),

                timestamp=last["timestamp"],

                exit_reason="END_OF_BACKTEST"
            )

        # -----------------------------------------------------
        # Performance analysis
        # -----------------------------------------------------

        metrics = PerformanceAnalyzer(

            trades=self.portfolio.trade_history,

            equity_curve=self.equity_curve

        ).analyze()

        # -----------------------------------------------------
        # Return result
        # -----------------------------------------------------

        return {

            "trades":
                self.portfolio.trade_history,

            "metrics":
                metrics

        }