from typing import Any
from pydantic import BaseModel


class IndicatorConfig(BaseModel):
    type: str
    parameters: dict[str, Any] = {}
