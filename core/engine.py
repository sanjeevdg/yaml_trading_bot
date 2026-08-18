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

    def calculate_risk_levels(self, price,signal):


        current_price = self.broker.latest_price(signal.symbol)

        stop_loss, take_profit = self.calculate_risk_levels(
            current_price,signal
        )

        print(
            f">>> {signal.symbol} "
            f"signal={signal.price} "
            f"current={current_price} "
            f"SL={stop_loss} "
            f"TP={take_profit}"
        )


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



    def execute(self, df):

        signal = self.strategy.evaluate(df)

        if signal.action == "HOLD":
            return {
                "status": "no_trade",
                "signal": signal
            }

        # Connect to paper broker
        self.broker.connect()

        if signal.action.value == "BUY":

            stop_loss, take_profit = self.calculate_risk_levels(
                signal.price,signal
            )
            print(
                f">>> {signal.symbol} "
                f"entry={signal.price} "
                f"SL={stop_loss} "
                f"TP={take_profit}"
            )
            result = self.broker.buy(
                signal.symbol,
                qty=1,
                stop_loss=stop_loss,
                take_profit=take_profit
            )

        elif signal.action.value == "SELL":

            result = self.broker.sell(
                signal.symbol,
                qty=1
            )

        elif signal.action.value == "HOLD":

            return {
                "status": "no_trade",
                "signal": signal
            }

        else:

            return {
                "status": "ignored",
                "signal": signal
            }

        
        return {
            "status": "submitted",
            "signal": signal,
            "order": result
        }    

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

            quantity=1,
            risk=self.cfg.risk
        )

        if mode == "signal":

            result = self.strategy.evaluate(df)

        elif mode == "backtest":

            backtester = BacktestEngine(
                strategy=self.strategy,
                risk=self.cfg.risk.model_dump(
                    exclude_none=True
                )
            )

            result = backtester.run(df)

            return result    
        elif mode == "optimize":

            optimizer = Optimizer(
                strategy=self.strategy,
                config=self.cfg
            )

            return optimizer.run(df)    
        elif mode == "paper":

            result = self.execute(df)

            return result            
        else:

            raise ValueError(f"Unknown mode: {mode}")

        return result
