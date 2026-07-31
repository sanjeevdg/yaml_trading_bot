from .ema_cross import EMACrossStrategy


class StrategyFactory:

    @staticmethod
    def create(config):

        if config.type == "ema_cross":

            return EMACrossStrategy(
                **config.parameters
            )

        raise ValueError(
            f"Unknown strategy: {config.type}"
        )
