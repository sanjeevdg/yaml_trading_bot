from .alpaca import AlpacaBroker


class BrokerFactory:

    @staticmethod
    def create(config):

        if config.provider == "alpaca":
            return AlpacaBroker()

        raise ValueError(f"Unknown broker: {config.provider}")
