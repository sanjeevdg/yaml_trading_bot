#!/usr/bin/env python3

import argparse

from rich import print

from core import ConfigLoader
from core.engine import TradingEngine
from core.logger import BotLogger

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_paper_dashboard(results, broker):

    console.print()
    console.print(
        Panel(
            "[bold cyan]YAML TRADING BOT[/bold cyan]\n"
            "[yellow]PAPER TRADING[/yellow]",
            expand=False
        )
    )

    # Account summary
    try:
        account = broker.account()

        equity = float(account.equity)
        cash = float(account.cash)
        previous_equity = float(account.last_equity)
        day_pl = equity - previous_equity

        account_table = Table(title="Account Summary")
        account_table.add_column("Metric")
        account_table.add_column("Value", justify="right")

        account_table.add_row("Equity", f"${equity:,.2f}")
        account_table.add_row("Cash", f"${cash:,.2f}")
        account_table.add_row(
            "Day P/L",
            f"${day_pl:+,.2f}"
        )

        console.print(account_table)

    except Exception as exc:
        console.print(
            f"[yellow]Account summary unavailable: {exc}[/yellow]"
        )

    # Signals and order results
    order_table = Table(title="Trading Results")
    order_table.add_column("Symbol")
    order_table.add_column("Signal")
    order_table.add_column("Price", justify="right")
    order_table.add_column("Result")
    order_table.add_column("Order Status")
    order_table.add_column("Limit Price", justify="right")
    order_table.add_column("Stop-Loss", justify="right")
    order_table.add_column("Take-Profit", justify="right")

    for item in results:
        signal = item.get("signal")

        if signal is None:
            continue

        
        order = item.get("order")
        action = getattr(signal.action, "value", signal.action)
        status = item.get("status", "unknown")
        order_status = "-"
        limit_price = "-"

        # Refresh the order from Alpaca to get its latest status
        if order is not None:
            try:
                order = broker.client.get_order_by_id(order.id)
            except Exception as exc:
                console.print(
                    f"[yellow]Could not refresh order "
                    f"for {signal.symbol}: {exc}[/yellow]"
                )

            order_status = str(
                getattr(order.status, "value", order.status)
            ).lower()

            if order_status == "filled":
                status = "filled"
            elif order_status == "partially_filled":
                status = "partially_filled"
            elif order_status in {
                "rejected", "canceled", "cancelled", "expired"
            }:
                status = order_status
            else:
                status = "submitted"

            if order.limit_price is not None:
                limit_price = f"${float(order.limit_price):.2f}"




        if order is not None:
            order_status = str(
                getattr(order.status, "value", order.status)
            )

            if order.limit_price is not None:
                limit_price = f"${float(order.limit_price):.2f}"

        
        stop_loss = item.get("stop_loss")
        take_profit = item.get("take_profit")

        stop_loss_text = (
            f"${float(stop_loss):.2f}"
            if stop_loss is not None
            else "-"
        )

        take_profit_text = (
            f"${float(take_profit):.2f}"
            if take_profit is not None
            else "-"
        )        




        order_table.add_row(
            signal.symbol,
            str(action),
            f"${float(signal.price):.2f}",
            str(status),
            order_status,
            limit_price,
            stop_loss_text,
            take_profit_text
        )

    console.print(order_table)

    # Current positions
    try:
        positions = broker.positions()

        position_table = Table(title="Current Positions")
        position_table.add_column("Symbol")
        position_table.add_column("Qty", justify="right")
        position_table.add_column("Market Value", justify="right")
        position_table.add_column("Unrealized P/L", justify="right")

        for position in positions:
            position_table.add_row(
                position.symbol,
                str(position.qty),
                f"${float(position.market_value):,.2f}",
                f"${float(position.unrealized_pl):+,.2f}"
            )

        console.print(position_table)

        if not positions:
            console.print("[dim]No open positions.[/dim]")

    except Exception as exc:
        console.print(
            f"[yellow]Positions unavailable: {exc}[/yellow]"
        )


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
        show_paper_dashboard(result, engine.broker)
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