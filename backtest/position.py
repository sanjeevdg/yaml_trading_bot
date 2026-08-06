from dataclasses import dataclass


@dataclass
class Position:

    symbol: str

    quantity: int

    entry_price: float

    entry_time: object
