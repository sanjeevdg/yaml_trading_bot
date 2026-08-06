from .trade import Trade


class ExecutionSimulator:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def execute_buy(

        self,

        symbol,

        price,

        quantity,

        timestamp

    ):

        return self.portfolio.buy(

            symbol,

            price,

            quantity,

            timestamp

        )

    def execute_sell(

        self,

        symbol,

        price,

        timestamp

    ):

        result = self.portfolio.sell(

            symbol,

            price

        )

        if result is None:

            return None

        position, pnl = result

        trade = Trade(

            symbol=symbol,

            entry_time=position.entry_time,

            exit_time=timestamp,

            entry_price=position.entry_price,

            exit_price=price,

            quantity=position.quantity,

            pnl=pnl

        )

        self.portfolio.trade_history.append(trade)

        return trade
