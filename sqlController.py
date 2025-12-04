import sqlite3 as sql

def initialize_database(name):

    conn = sql.connect('SolanaStake.db')

    cursor = conn.cursor()

    # epoch
    # activated_stake: amount of stake in solona at the end of the epoch
    # action: Buy Solona, Sell the Solana I have, Do nothing
    # trade_id, unique identifier to send to coinbase
    cursor.execute("CREATE TABLE history(epoch, activated_stake, action, trade_id)")

def update_table(buy_sell_hold):

    #If buy 
    if buy_sell_hold == 'buy':
        pass
    elif buy_sell_hold == 'sell':
        pass
    #If hold
    else:
        pass
