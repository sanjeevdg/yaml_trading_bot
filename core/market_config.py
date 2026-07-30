from pydantic import BaseModel


class MarketConfig(BaseModel):

    provider: str

    symbols: list[str]

    timeframe: str
