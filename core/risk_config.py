from pydantic import BaseModel


class PositionSize(BaseModel):
    type: str
    amount: float


class RiskConfig(BaseModel):

    position_size: PositionSize

    stop_loss: float

    take_profit: float
