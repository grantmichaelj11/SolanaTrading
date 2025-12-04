from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
from decimal import Decimal, ROUND_DOWN
load_dotenv()


class coinbaseConnector:

    def __init__(self):

        self.client = RESTClient(api_key=os.getenv('CDP_API_KEY_ID'), api_secret=os.getenv('CDP_API_KEY_SECRET'))

    def buy_order(self, order_id, product_id='SOL-USD'):

        #Get total USD
        raw_amount = Decimal(self.client.get_account('b1deda06-27ae-5106-bfd2-cff9c88b865a')['account']['available_balance']['value'])
        usd_amount = raw_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        buy_order = self.client.market_order_buy(client_order_id=order_id, product_id=product_id, quote_size=f"{usd_amount}")

        return buy_order

    def sell_order(self, order_id, product_id='SOL-USD', amount=0):

        #Get total Solana
        account = self.client.get_account('9e6453ec-530c-5fed-8551-55ba3f88f5bb')['account']
        amount = str(round(float(account.available_balance['value']), 7))[:-1]

        #Sell Solana
        sell_order = self.client.market_order_sell(client_order_id=order_id, product_id=product_id, base_size=amount)

        #Return Sell Order
        return sell_order

