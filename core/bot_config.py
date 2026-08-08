from typing import Optional

from pydantic import BaseModel, Field

from .broker_config import BrokerConfig
from .market_config import MarketConfig
from .indicator_config import IndicatorConfig
from .strategy_config import StrategyConfig
from .risk_config import RiskConfig
from .schedule_config import ScheduleConfig


class BotConfig(BaseModel):

    broker: BrokerConfig

    market: MarketConfig

    indicators: list[IndicatorConfig]

    strategy: StrategyConfig

    optimize: dict = Field(
        default_factory=dict
    )

    risk: Optional[RiskConfig] = None

    schedule: Optional[ScheduleConfig] = None

