#!/usr/bin/env python3

import argparse

from rich import print

from core import ConfigLoader
from core.logger import BotLogger

from brokers.factory import BrokerFactory
from data.factory import MarketDataFactory


def main():

    #
    # Logger
    #
    BotLogger.configure()

    #
    # Command line
    #
    parser = argparse.ArgumentParser(
        description="YAML Trading Bot"
    )

    parser.add_argument(
        "config",
        help="Configuration YAML"
    )

    args = parser.parse_args()

    #
    # Load configuration
    #
    cfg = ConfigLoader.load(args.config)

    BotLogger.success("Configuration loaded")

    #
    # Broker
    #
    broker = BrokerFactory.create(cfg.broker)

    broker.connect()

    BotLogger.success("Broker connected")

    #
    # Market Data
    #
    market = MarketDataFactory.create(cfg.market)

    BotLogger.success("Market provider ready")

    #
    # Download bars
    #
    df = market.get_bars(

        symbol=cfg.market.symbols[0],

        timeframe=cfg.market.timeframe,

        limit=10

    )

    from indicators.engine import IndicatorEngine

    engine = IndicatorEngine()

    df = engine.add_ema(df, 10)

    print(
        df[
            [
                "timestamp",
                "close",
                "EMA_10"
            ]
        ].tail(10)
    )


if __name__ == "__main__":
    main()
