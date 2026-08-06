class Statistics:

    @staticmethod
    def win_rate(trades):

        if not trades:
            return 0

        wins = sum(1 for t in trades if t.pnl > 0)

        return wins / len(trades)

    @staticmethod
    def gross_profit(trades):

        return sum(t.pnl for t in trades if t.pnl > 0)

    @staticmethod
    def gross_loss(trades):

        return abs(sum(t.pnl for t in trades if t.pnl < 0))
