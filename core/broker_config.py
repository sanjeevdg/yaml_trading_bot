from typing import Literal
from pydantic import BaseModel


class BrokerConfig(BaseModel):
    provider: Literal["alpaca"]
    paper: bool = True
