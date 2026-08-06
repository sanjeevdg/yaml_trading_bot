class Metrics:

    @staticmethod
    def profit_factor(trades):

        gp = sum(t.pnl for t in trades if t.pnl > 0)

        gl = abs(sum(t.pnl for t in trades if t.pnl < 0))

        if gl == 0:
            return 999

        return gp / gl