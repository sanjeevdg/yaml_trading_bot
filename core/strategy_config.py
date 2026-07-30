from typing import Any
from pydantic import BaseModel


class StrategyDefinition(BaseModel):
    type: str

    parameters: dict[str, Any] = {}
