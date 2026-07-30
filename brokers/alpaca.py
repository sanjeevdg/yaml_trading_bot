from dotenv import load_dotenv
import os

from alpaca.trading.client import TradingClient

from .base import Broker

load_dotenv()


class AlpacaBroker(Broker):

    def __init__(self):

        self.client = None

    def connect(self):

        key = os.getenv("ALPACA_API_KEY")
        secret = os.getenv("ALPACA_SECRET_KEY")

        paper = os.getenv("PAPER", "True").lower() == "true"

        self.client = TradingClient(
            api_key=key,
            secret_key=secret,
            paper=paper
        )

        return self.client

    def account(self):

        return self.client.get_account()

    def positions(self):

        return self.client.get_all_positions()

    def bars(self, *args, **kwargs):
        raise NotImplementedError()

    def latest_price(self, *args, **kwargs):
        raise NotImplementedError()

    def buy(self, *args, **kwargs):
        raise NotImplementedError()

    def sell(self, *args, **kwargs):
        raise NotImplementedError()

    def close(self, *args, **kwargs):
        raise NotImplementedError()
