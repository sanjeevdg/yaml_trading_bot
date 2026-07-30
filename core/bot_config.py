from pydantic import BaseModel

from .broker_config import BrokerConfig
from .market_config import MarketConfig
from .strategy_config import StrategyDefinition
from .risk_config import RiskConfig
from .schedule_config import ScheduleConfig

from .indicator_config import IndicatorConfig

class BotConfig(BaseModel):
    broker: BrokerConfig
    market: MarketConfig
    indicators: list[IndicatorConfig] = []
    strategy: StrategyDefinition
    risk: RiskConfig
    schedule: ScheduleConfig

