from pathlib import Path

import yaml

from .bot_config import BotConfig


class ConfigLoader:

    @staticmethod
    def load(filename: str) -> BotConfig:

        path = Path(filename)

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        return BotConfig(**data)
