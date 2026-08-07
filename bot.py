#!/usr/bin/env python3

import argparse

from rich import print

from core import ConfigLoader
from core.engine import TradingEngine
from core.logger import BotLogger


def main():

    BotLogger.configure()

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "config",
        help="YAML configuration file"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--signal",
        action="store_true",
        help="Generate latest signal"
    )

    group.add_argument(
        "--backtest",
        action="store_true",
        help="Run backtest"
    )

    group.add_argument(
        "--optimize",
        action="store_true",
        help="Optimize strategy parameters"
    )

    args = parser.parse_args()

    cfg = ConfigLoader.load(args.config)

    BotLogger.success("Configuration loaded")

    engine = TradingEngine(cfg)

    #
    # Determine execution mode
    #

    if args.optimize:
        mode = "optimize"
    elif args.backtest:
        mode = "backtest"
    else:
        mode = "signal"

    result = engine.run(mode=mode)

    #
    # Signal Mode
    #

    if mode == "signal":

        print(result)

    #
    # Backtest Mode
    #

    elif mode == "backtest":

        trades = result

        wins = sum(1 for t in trades if t.pnl > 0)
        losses = len(trades) - wins
        net = sum(t.pnl for t in trades)

        print()

        print(f"Trades : {len(trades)}")
        print(f"Wins   : {wins}")
        print(f"Losses : {losses}")
        print(f"Net P/L: ${net:.2f}")

        if trades:

            print("\nLast 5 Trades:\n")

            for trade in trades[-5:]:

                print(trade)

    #
    # Optimization Mode
    #

    elif mode == "optimize":

        results = result

        print()

        print(f"Parameter combinations tested : {len(results)}")

        print()

        print(
            f"{'Rank':<5}"
            f"{'Parameters':<30}"
            f"{'Trades':>8}"
            f"{'Win %':>10}"
            f"{'Net Profit':>15}"
        )

        print("-" * 75)

        for i, r in enumerate(results[:10], start=1):

            print(
                f"{i:<5}"
                f"{str(r.parameters):<30}"
                f"{r.trades:>8}"
                f"{r.win_rate:>10.2f}"
                f"{r.net_profit:>15.2f}"
            )


if __name__ == "__main__":
    main()