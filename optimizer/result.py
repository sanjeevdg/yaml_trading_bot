from dataclasses import dataclass


@dataclass
class OptimizationResult:

    parameters: dict

    trades: int

    wins: int

    losses: int

    net_profit: float

    win_rate: float

    profit_factor: float


