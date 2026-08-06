from .ema_cross import EMACrossStrategy
from .rsi import RSIStrategy
from .macd import MACDStrategy


class StrategyFactory:

    @staticmethod
    def create(config):

        if config.type == "ema_cross":

            return EMACrossStrategy(
                **config.parameters
            )

        if config.type == "rsi":

            return RSIStrategy(
                **config.parameters
            )

        if config.type == "macd":

            return MACDStrategy()

        raise ValueError(
            f"Unknown strategy: {config.type}"
        )
