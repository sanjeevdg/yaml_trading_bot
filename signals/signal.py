from dataclasses import dataclass
from enum import Enum


class Action(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"


@dataclass
class Signal:

    action: Action

    symbol: str

    reason: str

    price: float
