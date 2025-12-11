from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
from decimal import Decimal, ROUND_DOWN
load_dotenv()


class coinbaseConnector:

    def __init__(self):

        self.client = RESTClient(api_key=os.getenv('CDP_API_KEY_ID'), api_secret=os.getenv('CDP_API_KEY_SECRET'))

    def get_solana_price(self):

        product = self.client.get_product('SOL-USD')
        
        return Decimal(product.price)
    
    def get_fee_for_transaction(self):

        fee = self.client.get_transaction_summary()['fee_tier']['taker_fee_rate']
        
        return Decimal(fee)


    def buy_order_limit(self, order_id, product_id='SOL-USD'):

        #Get total USD
        raw_amount = Decimal(self.client.get_account('b1deda06-27ae-5106-bfd2-cff9c88b865a')['account']['available_balance']['value'])
        usd_amount = raw_amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

        fee_rate = self.get_fee_for_transaction()
        current_price = self.get_solana_price()

        max_safe_usd = usd_amount * (Decimal(1) - fee_rate)

        order_size = Decimal(max_safe_usd/current_price).quantize(Decimal("0.000001"), rounding=ROUND_DOWN) #Limit Price

        if usd_amount == 0:
            return 'HOLD'

        else:
            buy_order = self.client.limit_order_gtc_buy(client_order_id=order_id, product_id=product_id, base_size=f"{order_size}", limit_price=f"{current_price}")
            return buy_order

    def sell_order(self, order_id, product_id='SOL-USD'):

        #Get total Solana
        account = self.client.get_account('9e6453ec-530c-5fed-8551-55ba3f88f5bb')['account']
        amount = str(round(float(account.available_balance['value']), 7))[:-1]

        if amount == 0:
            return 'HOLD'

        else:
            #Sell Solana
            sell_order = self.client.market_order_sell(client_order_id=order_id, product_id=product_id, base_size=amount)

            #Return Sell Order
            return sell_order

