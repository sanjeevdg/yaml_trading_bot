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
    group.add_argument(
        "--paper",
        action="store_true",
        help="Run live market trading using Alpaca paper account"
    )
    args = parser.parse_args()

    cfg = ConfigLoader.load(args.config)

    BotLogger.success("Configuration loaded")
    print(">>> Creating TradingEngine")
    engine = TradingEngine(cfg)
    print(">>> TradingEngine created")

    #
    # Determine execution mode
    #
    def execute(self):

        signal = self.generate_signal()

        # No trade
        if signal.action == "HOLD":
            return {
                "status": "no_trade",
                "signal": signal
            }

        # Connect to Alpaca paper
        self.broker.connect()

        # Get current position
        positions = self.broker.positions()

        # Your risk checks go here
        # ...

        if signal.action == "BUY":

            result = self.broker.buy(
                signal.symbol,
                qty=1
            )

        elif signal.action == "SELL":

            result = self.broker.sell(
                signal.symbol,
                qty=1
            )

        else:
            return {
                "status": "ignored",
                "signal": signal
            }

        return {
            "status": "submitted",
            "signal": signal,
            "order": result
        }
    if args.optimize:
        mode = "optimize"
    elif args.backtest:
        mode = "backtest"
    elif args.paper:
        mode = "paper"    
    else:
        mode = "signal"
    print(f">>> Execution mode: {mode}")

    print(">>> Calling engine.run()")    
    result = engine.run(mode=mode)
    print(">>> engine.run() completed")
    #
    # Signal Mode
    #
    if mode == "paper":
        print(">>> PAPER RESULT")
        print(result)
    elif mode == "signal":

        print(result)

    #
    # Backtest Mode
    #

    elif mode == "backtest":

        for item in result:

            symbol = item["symbol"]
            backtest_result = item["result"]

            trades = backtest_result["trades"]
            metrics = backtest_result["metrics"]

            print()
            print("=" * 60)
            print(f"BACKTEST RESULTS: {symbol}")
            print("=" * 60)

            print()

            print(f"Trades        : {metrics['trades']}")
            print(f"Wins          : {metrics['wins']}")
            print(f"Losses        : {metrics['losses']}")
            print(f"Win Rate      : {metrics['win_rate']:.2f}%")

            print(f"Gross Profit  : ${metrics['gross_profit']:.2f}")
            print(f"Gross Loss    : ${metrics['gross_loss']:.2f}")
            print(f"Net P/L       : ${metrics['net_profit']:.2f}")

            profit_factor = metrics["profit_factor"]

            if profit_factor == float("inf"):
                print("Profit Factor : ∞")
            else:
                print(f"Profit Factor : {profit_factor:.2f}")

            print(f"Average Trade : ${metrics['average_trade']:.2f}")
            print(f"Average Win   : ${metrics['average_win']:.2f}")
            print(f"Average Loss  : ${metrics['average_loss']:.2f}")

            print(f"Largest Win   : ${metrics['largest_win']:.2f}")
            print(f"Largest Loss  : ${metrics['largest_loss']:.2f}")

            print(f"Max Drawdown  : ${metrics['max_drawdown']:.2f}")

            if trades:

                print("\nLast 5 Trades:\n")

                for trade in trades[-5:]:
                    print(trade)

            else:

                print("\nNo trades generated.")

    #
    # Optimization Mode
    #

    elif mode == "optimize":

        for item in result:

            symbol = item["symbol"]
            results = item["result"]

            print()
            print("=" * 75)
            print(f"OPTIMIZATION RESULTS: {symbol}")
            print("=" * 75)

            print()
            print(
                f"Parameter combinations tested : {len(results)}"
            )

            print()

            print(
                f"{'Rank':<5}"
                f"{'Parameters':<30}"
                f"{'Trades':>8}"
                f"{'Win %':>10}"
                f"{'Net Profit':>15}"
            )

            print("-" * 75)

            for i, r in enumerate(
                results[:10],
                start=1
            ):

                print(
                    f"{i:<5}"
                    f"{str(r.parameters):<30}"
                    f"{r.trades:>8}"
                    f"{r.win_rate:>10.2f}"
                    f"{r.net_profit:>15.2f}"
                )


if __name__ == "__main__":
    main()