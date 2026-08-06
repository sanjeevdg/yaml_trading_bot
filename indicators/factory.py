from .ema import EMA
from .rsi import RSI
from .macd import MACDIndicator
from .atr import ATR
from .bollinger import Bollinger
from .supertrend import SuperTrend


class IndicatorFactory:

    @staticmethod
    def create(config):

        indicator_type = config.type.lower()

        params = config.parameters

        if indicator_type == "ema":
            return EMA(
                period=params.get("period", 20)
            )

        if indicator_type == "rsi":
            return RSI(
                period=params.get("period", 14)
            )

        if indicator_type == "macd":
            return MACDIndicator(
                fast=params.get("fast", 12),
                slow=params.get("slow", 26),
                signal=params.get("signal", 9),
            )

        if indicator_type == "atr":
            return ATR(
                period=params.get("period", 14)
            )

        if indicator_type == "bollinger":
            return Bollinger(
                period=params.get("period", 20),
                stddev=params.get("stddev", 2),
            )
        if indicator_type == "supertrend":

            return SuperTrend(

                period=params.get("period", 10),

                multiplier=params.get("multiplier", 3)

            )    

        raise ValueError(f"Unknown indicator: {indicator_type}")