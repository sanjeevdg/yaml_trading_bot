#!/usr/bin/env python3

import argparse

from rich import print

from core import ConfigLoader
from core.engine import TradingEngine
from core.logger import BotLogger
from rich.table import Table


def main():

    BotLogger.configure()

    parser = argparse.ArgumentParser()

    parser.add_argument("config")

    args = parser.parse_args()

    cfg = ConfigLoader.load(args.config)

    BotLogger.success("Configuration loaded")

    engine = TradingEngine(cfg)

    signal = engine.run()


    table = Table(title="Signal")

    table.add_column("Field")
    table.add_column("Value")

    table.add_row("Action", signal.action.value)
    table.add_row("Symbol", signal.symbol)
    table.add_row("Price", f"{signal.price:.2f}")
    table.add_row("Confidence", f"{signal.confidence:.2f}")
    table.add_row("Reason", signal.reason)

    for k, v in signal.indicators.items():
        table.add_row(k, str(v))

    print(table)


if __name__ == "__main__":
    main()
