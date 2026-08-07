from rich import print

from brokers.factory import BrokerFactory
from data.factory import MarketDataFactory

from indicators.engine import IndicatorEngine
from indicators.ema import EMA

#from strategies.ema_cross import EMACrossStrategy
from strategies.factory import StrategyFactory
from backtest.engine import BacktestEngine
from optimizer.engine import Optimizer


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

        self.indicators = IndicatorEngine()

        self.strategy = StrategyFactory.create(
            config.strategy
        )

    def run(self, mode="signal"):

        #
        # Connect
        #

        self.broker.connect()

        #
        # Download bars
        #

        df = self.market.get_bars(

            symbol=self.cfg.market.symbols[0],

            timeframe=self.cfg.market.timeframe,

            limit=300

        )

        #
        # Indicators
        #

        from indicators.factory import IndicatorFactory

        for indicator_cfg in self.cfg.indicators:

            indicator = IndicatorFactory.create(
                indicator_cfg.model_dump(exclude_none=True)
            )

            self.indicators.add(indicator)

        df = self.indicators.apply(df)

        #
        # Strategy
        #

        

        backtester = BacktestEngine(
            strategy=self.strategy,

            initial_cash=10000,

            quantity=1
        )

        if mode == "signal":

            result = self.strategy.evaluate(df)

        elif mode == "backtest":

            backtester = BacktestEngine(
                strategy=self.strategy
            )

            result = backtester.run(df)

            print(f"\nCompleted Backtest: {len(result)}")

            if result:

                print("\nLast 5 Trades:\n")

                for trade in result[-5:]:

                    print(trade)
        elif mode == "optimize":

            optimizer = Optimizer(
                strategy=self.strategy,
                config=self.cfg
            )

            return optimizer.run(df)            
        else:

            raise ValueError(f"Unknown mode: {mode}")

        return result
