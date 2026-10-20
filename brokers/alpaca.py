from dotenv import load_dotenv
import os
from decimal import Decimal, ROUND_HALF_UP
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from .base import Broker
from alpaca.trading.requests import (
    MarketOrderRequest,
    TakeProfitRequest,
    StopLossRequest,
)
from alpaca.trading.requests import LimitOrderRequest
from alpaca.trading.enums import (
    OrderSide,
    TimeInForce,
)
from alpaca.data.historical import StockHistoricalDataClient

from alpaca.data.requests import StockLatestQuoteRequest
load_dotenv()


class AlpacaBroker(Broker):

    def __init__(self):

        self.client = None

    def connect(self):

        key = os.getenv("ALPACA_API_KEY")
        secret = os.getenv("ALPACA_SECRET_KEY")

        if not key:
            raise RuntimeError(
                "ALPACA_API_KEY is not set"
            )

        if not secret:
            raise RuntimeError(
                "ALPACA_SECRET_KEY is not set"
            )

        paper = os.getenv("PAPER", "true").lower() == "true"

        self.client = TradingClient(
            api_key=key,
            secret_key=secret,
            paper=paper
        )
        self.data_client = StockHistoricalDataClient(
            key,
            secret
        )
        return self.client, self.data_client

    def account(self):

        return self.client.get_account()

    def positions(self):

        return self.client.get_all_positions()

    def bars(self, *args, **kwargs):
        raise NotImplementedError()

    def latest_price(self, symbol: str) -> float:
        request = StockLatestQuoteRequest(
            symbol_or_symbols=symbol
        )

        quotes = self.data_client.get_stock_latest_quote(request)

        quote = quotes[symbol]

        return float(quote.ask_price)

    

    def buy(
        self,
        symbol: str,
        qty: float,
        entry_price: float,
        stop_loss: float | None = None,
        take_profit: float | None = None
    ):



        entry_price = float(
            Decimal(str(entry_price)).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP
            )
        )

        if stop_loss is not None:
            stop_loss = round(float(stop_loss), 2)

        if take_profit is not None:
            take_profit = round(float(take_profit), 2)







        order = LimitOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            limit_price=entry_price
        )

        if stop_loss is not None and take_profit is not None:

            order.order_class = "bracket"

            order.take_profit = TakeProfitRequest(
                limit_price=take_profit
            )

            order.stop_loss = StopLossRequest(
                stop_price=stop_loss
            )

        return self.client.submit_order(
            order_data=order
        )



    def sell(self, symbol: str, qty: float):

        order = MarketOrderRequest(
            symbol=symbol,
            qty=qty,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )

        return self.client.submit_order(order_data=order)
        
    def close(self, *args, **kwargs):
        raise NotImplementedError()
