from pathlib import Path
import sys

from loguru import logger


class BotLogger:

    _configured = False

    @classmethod
    def configure(cls):

        if cls._configured:
            return

        Path("logs").mkdir(exist_ok=True)

        logger.remove()

        #
        # Console logging
        #
        logger.add(
            sys.stdout,
            level="INFO",
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{message}</cyan>"
            )
        )

        #
        # Log file
        #
        logger.add(
            "logs/trading.log",
            level="DEBUG",
            rotation="10 MB",
            retention=10,
            compression="zip",
            enqueue=True
        )

        cls._configured = True

    @staticmethod
    def info(message):
        logger.info(message)

    @staticmethod
    def warning(message):
        logger.warning(message)

    @staticmethod
    def error(message):
        logger.error(message)

    @staticmethod
    def debug(message):
        logger.debug(message)

    @staticmethod
    def success(message):
        logger.success(message)
