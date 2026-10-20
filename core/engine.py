from rich import print

from brokers.factory import BrokerFactory
from data.factory import MarketDataFactory

from indicators.engine import IndicatorEngine
from indicators.ema import EMA

#from strategies.ema_cross import EMACrossStrategy
from strategies.factory import StrategyFactory
from backtest.engine import BacktestEngine
from optimizer.engine import Optimizer
from signals.signal import Signal, Action
from rich.progress import Progress, SpinnerColumn, BarColumn
from rich.progress import TextColumn, TimeElapsedColumn


class TradingEngine:

    def __init__(self, config):

        self.cfg = config

        #
        # Services
        #

        self.broker = BrokerFactory.create(
            config.broker
        )

        self.market = MarketDataFactory.create(
            config.market
        )

        indicators = IndicatorEngine()

        self.strategy = StrategyFactory.create(
            config.strategy
        )

    def calculate_risk_levels(self, signal):

        entry_price = float(signal.price)

        risk = self.cfg.risk.model_dump(
            exclude_none=True
        )

        stop_loss_percent = risk.get("stop_loss")
        take_profit_percent = risk.get("take_profit")

        stop_loss = None
        take_profit = None

        if stop_loss_percent is not None:
            stop_loss = round(
                entry_price * (
                    1 - float(stop_loss_percent) / 100
                ),
                2
            )

        if take_profit_percent is not None:
            take_profit = round(
                entry_price * (
                    1 + float(take_profit_percent) / 100
                ),
                2
            )

        print(
            f">>> {signal.symbol} "
            f"entry={entry_price:.2f} "
            f"SL={stop_loss:.2f} "
            f"TP={take_profit:.2f}"
        )

        return stop_loss, take_profit



    def execute(self, df):

        signal = self.strategy.evaluate(df)

        if signal.action == "HOLD":
            return {
                "status": "no_trade",
                "signal": signal
            }

        # Connect to paper broker
        self.broker.connect()
        # Default risk levels for signals without calculated levels
        stop_loss = None
        take_profit = None
        if signal.action.value == "BUY":

            entry_price = float(signal.price)

            stop_loss, take_profit = self.calculate_risk_levels(
                signal
            )

            print(
                f">>> {signal.symbol} "
                f"entry={entry_price} "
                f"SL={stop_loss} "
                f"TP={take_profit}"
            )

            result = self.broker.buy(
                signal.symbol,
                qty=1,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit
            )

        elif signal.action.value == "SELL":

            positions = self.broker.positions()

            position = next(
                (
                    p for p in positions
                    if p.symbol == signal.symbol
                ),
                None
            )

            if position is None:

                print(
                    f">>> {signal.symbol} SELL ignored - "
                    f"no existing long position"
                )

                return {
                    "status": "no_position",
                    "signal": signal
                }

            qty = abs(float(position.qty))

            result = self.broker.sell(
                signal.symbol,
                qty=qty
            )

        else:

            return {
                "status": "ignored",
                "signal": signal
            }

        return {
            "status": "submitted",
            "signal": signal,
            "order": result,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }   

    
    def run(self, mode="signal"):

        self.broker.connect()

        results = []
        symbols = self.cfg.market.symbols

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn()
        ) as progress:

            task = progress.add_task(
                "Preparing...",
                total=len(symbols)
            )

            for symbol in symbols:

                progress.update(
                    task,
                    description=f"Processing {symbol}"
                )

                print(f"\n{'=' * 60}")
                print(f"Processing {symbol}")
                print(f"{'=' * 60}")

                # Download bars for this symbol
                df = self.market.get_bars(
                    symbol=symbol,
                    timeframe=self.cfg.market.timeframe,
                    limit=300
                )

                # Create indicators
                from indicators.factory import IndicatorFactory

                # Create a fresh indicator engine for each symbol
                indicators = IndicatorEngine()

                for indicator_cfg in self.cfg.indicators:

                    indicator = IndicatorFactory.create(
                        indicator_cfg.model_dump(
                            exclude_none=True
                        )
                    )

                    indicators.add(indicator)

                df = indicators.apply(df)

                # SIGNAL
                if mode == "signal":

                    signal = self.strategy.evaluate(df)
                    results.append(signal)

                # BACKTEST
                elif mode == "backtest":

                    backtester = BacktestEngine(
                        strategy=self.strategy,
                        cfg=self.cfg,
                        initial_cash=10000,
                        quantity=1,
                        risk=self.cfg.risk.model_dump(
                            exclude_none=True
                        )
                    )

                    result = backtester.run(df)

                    results.append({
                        "symbol": symbol,
                        "result": result
                    })

                # OPTIMIZE
                elif mode == "optimize":

                    optimizer = Optimizer(
                        strategy=self.strategy,
                        config=self.cfg
                    )

                    result = optimizer.run(df)

                    results.append({
                        "symbol": symbol,
                        "result": result
                    })

                # PAPER
                elif mode == "paper":

                    result = self.execute(df)
                    results.append(result)

                else:

                    raise ValueError(
                        f"Unknown mode: {mode}"
                    )

                # Advance after this symbol has been processed
                progress.update(task, advance=1)

        return results

