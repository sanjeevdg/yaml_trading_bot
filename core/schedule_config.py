from pydantic import BaseModel


class ScheduleConfig(BaseModel):
    interval: int
