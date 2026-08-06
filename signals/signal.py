from dataclasses import dataclass, field
from enum import Enum


class Action(Enum):

    BUY = "BUY"

    SELL = "SELL"

    HOLD = "HOLD"


@dataclass
class Signal:

    action: Action

    symbol: str

    price: float

    reason: str

    confidence: float = 1.0

    indicators: dict = field(default_factory=dict)