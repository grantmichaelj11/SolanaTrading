from coinbase.rest import RESTClient
from dotenv import load_dotenv
import os
load_dotenv()

def sell_order(order_id, product_id='SOL-USDC', amount=0):

    client = RESTClient(api_key=os.getenv('CDP_API_KEY_ID'), api_secret=os.getenv('CDP_API_KEY_SECRET'))

    sell_order = client.market_order_sell(client_order_id='test1', product_id='SOL-USDC', base_size='0.01')

    print(sell_order)