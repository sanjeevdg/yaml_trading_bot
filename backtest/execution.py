from .trade import Trade


class ExecutionSimulator:

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def execute_buy(
        self,
        symbol,
        price,
        quantity,
        timestamp,
        stop_loss=None,
        take_profit=None
    ):

        return self.portfolio.buy(
            symbol=symbol,
            price=price,
            quantity=quantity,
            timestamp=timestamp,
            stop_loss=stop_loss,
            take_profit=take_profit
        )

    def execute_sell(
        self,
        symbol,
        price,
        timestamp,
        exit_reason="STRATEGY"
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
            pnl=pnl,
            exit_reason=exit_reason
        )

        self.portfolio.trade_history.append(
            trade
        )

        return trade
