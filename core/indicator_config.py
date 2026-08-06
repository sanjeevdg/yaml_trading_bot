from typing import Any

from pydantic import BaseModel


class IndicatorConfig(BaseModel):

    type: str

    period: int | None = None

    fast: int | None = None

    slow: int | None = None

    signal: int | None = None
