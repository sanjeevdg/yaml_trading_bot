from typing import Any

from pydantic import BaseModel, Field


class StrategyConfig(BaseModel):

    type: str

    parameters: dict[str, Any] = Field(
        default_factory=dict
    )

    optimize: dict[str, Any] = Field(
        default_factory=dict
    )

    signals: dict[str, Any] = Field(
        default_factory=dict
    )