from .alpaca_data import AlpacaMarketData


class MarketDataFactory:

    @staticmethod
    def create(config):

        if config.provider == "alpaca":
            return AlpacaMarketData()

        raise ValueError(
            f"Unknown provider {config.provider}"
        )
