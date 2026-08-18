from .position import Position


class Portfolio:

    def __init__(self, initial_cash=10000):

        self.initial_cash = initial_cash

        self.cash = initial_cash

        self.positions = {}

        self.trade_history = []

        self.realized_pnl = 0

        self.unrealized_pnl = 0

        self.equity = initial_cash

    def has_position(self, symbol):

        return symbol in self.positions

    def buy(
        self,
        symbol,
        price,
        quantity,
        timestamp,
        stop_loss=None,
        take_profit=None
    ):

        cost = price * quantity

        if cost > self.cash:
            return False

        self.cash -= cost

        self.positions[symbol] = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            entry_time=timestamp,
            stop_loss=stop_loss,
            take_profit=take_profit
        )

        return True

    def sell(self, symbol, price):

        if symbol not in self.positions:
            return None

        position = self.positions.pop(symbol)

        proceeds = price * position.quantity

        pnl = (price - position.entry_price) * position.quantity

        self.cash += proceeds

        self.realized_pnl += pnl

        return position, pnl

    def update(self, prices):

        self.unrealized_pnl = 0

        value = self.cash

        for symbol, position in self.positions.items():

            if symbol not in prices:
                continue

            current = prices[symbol]

            pnl = (
                current - position.entry_price
            ) * position.quantity

            self.unrealized_pnl += pnl

            value += current * position.quantity

        self.equity = value

        return value