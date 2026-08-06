from .ema import EMA
from .rsi import RSI
from .macd import MACDIndicator


class IndicatorFactory:

    @staticmethod
    def create(config):

        indicator_type = config["type"].lower()

        if indicator_type == "ema":

            return EMA(config["period"])

        if indicator_type == "rsi":

            return RSI(
                config.get("period", 14)
            )

        if indicator_type == "macd":

            return MACDIndicator(
                fast=config.get("fast", 12),
                slow=config.get("slow", 26),
                signal=config.get("signal", 9)
            )

        raise ValueError(
            f"Unknown indicator: {indicator_type}"
        )
