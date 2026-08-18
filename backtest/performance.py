class PerformanceAnalyzer:

    def __init__(self, trades, equity_curve=None):

        self.trades = trades
        self.equity_curve = equity_curve or []

    def max_drawdown(self):

        if not self.equity_curve:
            return 0.0

        peak = self.equity_curve[0].equity
        max_drawdown = 0.0

        for point in self.equity_curve:

            equity = point.equity

            if equity > peak:
                peak = equity

            drawdown = peak - equity

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return max_drawdown

    def analyze(self):

        trades = self.trades

        total_trades = len(trades)

        wins = [
            trade
            for trade in trades
            if trade.pnl > 0
        ]

        losses = [
            trade
            for trade in trades
            if trade.pnl < 0
        ]

        gross_profit = sum(
            trade.pnl
            for trade in wins
        )

        gross_loss = sum(
            trade.pnl
            for trade in losses
        )

        net_profit = (
            gross_profit +
            gross_loss
        )

        win_rate = (
            100 * len(wins) / total_trades
            if total_trades
            else 0.0
        )

        if gross_loss < 0:

            profit_factor = (
                gross_profit /
                abs(gross_loss)
            )

        elif gross_profit > 0:

            profit_factor = float("inf")

        else:

            profit_factor = 0.0

        average_trade = (
            net_profit / total_trades
            if total_trades
            else 0.0
        )

        average_win = (
            gross_profit / len(wins)
            if wins
            else 0.0
        )

        average_loss = (
            gross_loss / len(losses)
            if losses
            else 0.0
        )

        largest_win = (
            max(
                trade.pnl
                for trade in wins
            )
            if wins
            else 0.0
        )

        largest_loss = (
            min(
                trade.pnl
                for trade in losses
            )
            if losses
            else 0.0
        )

        max_drawdown = self.max_drawdown()

        return {

            "trades": total_trades,

            "wins": len(wins),

            "losses": len(losses),

            "win_rate": win_rate,

            "gross_profit": gross_profit,

            "gross_loss": gross_loss,

            "net_profit": net_profit,

            "profit_factor": profit_factor,

            "average_trade": average_trade,

            "average_win": average_win,

            "average_loss": average_loss,

            "largest_win": largest_win,

            "largest_loss": largest_loss,

            "max_drawdown": max_drawdown,

        }