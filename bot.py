#!/usr/bin/env python3

import argparse

from core import ConfigLoader
from core.engine import TradingEngine

from core.logger import BotLogger


def main():

    BotLogger.configure()

    parser = argparse.ArgumentParser()

    parser.add_argument("config")

    args = parser.parse_args()

    cfg = ConfigLoader.load(args.config)

    BotLogger.success("Configuration loaded")

    engine = TradingEngine(cfg)

    engine.run()


if __name__ == "__main__":

    main()
