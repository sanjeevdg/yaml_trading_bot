from .ema_cross import EMACrossStrategy
from .rsi import RSIStrategy
from .macd import MACDStrategy
from .ema_rsi import EMARSIStrategy
from .bollinger import BollingerStrategy
from .atr_breakout import ATRBreakoutStrategy
from .ema_macd import EMAMACDStrategy
from .macd_rsi import MACDRSIStrategy
from .supertrend import SuperTrendStrategy
from .rules import RuleStrategy


STRATEGIES = {

    "ema_cross": EMACrossStrategy,
    "rsi": RSIStrategy,
    "macd": MACDStrategy,
    "ema_rsi": EMARSIStrategy,
    "bollinger": BollingerStrategy,
    "atr_breakout": ATRBreakoutStrategy,
    "ema_macd": EMAMACDStrategy,
    "macd_rsi": MACDRSIStrategy,
    "supertrend": SuperTrendStrategy,

    # Generic YAML-driven strategy
    "rules": RuleStrategy,
}


class StrategyFactory:

    @staticmethod
    def create(config):

        strategy_type = config.type.lower()

        strategy_cls = STRATEGIES.get(strategy_type)

        if strategy_cls is None:

            raise ValueError(
                f"Unknown strategy: {config.type}"
            )

        #
        # Generic YAML rule strategy
        #

        if strategy_type == "rules":

            return RuleStrategy(

                parameters=config.parameters or {},

                buy=config.buy or {},

                sell=config.sell or {}

            )

        #
        # Existing Python strategies
        #

        return strategy_cls(
            **config.parameters
        )