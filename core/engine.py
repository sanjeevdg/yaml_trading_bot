from rich import print

from brokers.factory import BrokerFactory
from data.factory import MarketDataFactory

from indicators.engine import IndicatorEngine
from indicators.ema import EMA

#from strategies.ema_cross import EMACrossStrategy
from strategies.factory import StrategyFactory

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

    def run(self):

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
                indicator_cfg
            )

            self.indicators.add(indicator)

        df = self.indicators.apply(df)

        #
        # Strategy
        #

        signal = self.strategy.evaluate(df)

        print(signal)

        return signal
