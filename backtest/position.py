from dataclasses import dataclass


@dataclass
class Position:

    symbol: str

    quantity: int

    entry_price: float

    entry_time: object

    stop_loss: float | None = None

    take_profit: float | None = None