from dataclasses import dataclass
from datetime import datetime


@dataclass
class Trade:

    symbol: str

    entry_time: datetime

    exit_time: datetime

    entry_price: float

    exit_price: float

    quantity: int

    pnl: float
