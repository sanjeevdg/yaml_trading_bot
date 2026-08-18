from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
import os


load_dotenv()


client = TradingClient(
    os.getenv("ALPACA_API_KEY"),
    os.getenv("ALPACA_SECRET_KEY"),
    paper=True
)

account = client.get_account()

print("Account:", account.account_number)
print("Status:", account.status)
print("Cash:", account.cash)
print("Buying power:", account.buying_power)