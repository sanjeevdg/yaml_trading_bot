from dataclasses import dataclass

from rich.console import Console
from rich.table import Table


@dataclass
class BacktestReport:

    trades: list

    def total_trades(self):

        return len(self.trades)

    def wins(self):

        return sum(1 for t in self.trades if t.pnl > 0)

    def losses(self):

        return sum(1 for t in self.trades if t.pnl <= 0)

    def win_rate(self):

        if not self.trades:
            return 0

        return self.wins() / len(self.trades) * 100

    def net_profit(self):

        return sum(t.pnl for t in self.trades)

    def average_win(self):

        wins = [t.pnl for t in self.trades if t.pnl > 0]

        if not wins:
            return 0

        return sum(wins) / len(wins)

    def average_loss(self):

        losses = [t.pnl for t in self.trades if t.pnl <= 0]

        if not losses:
            return 0

        return sum(losses) / len(losses)

    def profit_factor(self):

        gross_profit = sum(t.pnl for t in self.trades if t.pnl > 0)

        gross_loss = abs(
            sum(t.pnl for t in self.trades if t.pnl < 0)
        )

        if gross_loss == 0:
            return 999

        return gross_profit / gross_loss

    def show(self):

        console = Console()

        table = Table(title="Backtest Report")

        table.add_column("Metric")
        table.add_column("Value", justify="right")

        table.add_row("Trades", str(self.total_trades()))
        table.add_row("Wins", str(self.wins()))
        table.add_row("Losses", str(self.losses()))
        table.add_row("Win Rate", f"{self.win_rate():.2f}%")
        table.add_row("Net Profit", f"${self.net_profit():.2f}")
        table.add_row("Average Win", f"${self.average_win():.2f}")
        table.add_row("Average Loss", f"${self.average_loss():.2f}")
        table.add_row("Profit Factor", f"{self.profit_factor():.2f}")

        console.print(table)