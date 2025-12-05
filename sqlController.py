import sqlite3 as sql
import random
import string

def view_most_recent_stats():

    conn = sql.connect('SolanaStake.db')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM history ORDER BY epoch DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    return row

def initialize_database(epoch, stake):

    conn = sql.connect('SolanaStake.db')

    cursor = conn.cursor()

    # epoch
    # activated_stake: amount of stake in solona at the end of the epoch
    # action: Buy Solona, Sell the Solana I have, Do nothing
    # trade_id, unique identifier to send to coinbase
    cursor.execute("CREATE TABLE IF NOT EXISTS history(epoch, activated_stake, action, trade_id)")

    cursor.execute("SELECT 1 FROM history WHERE epoch = ?", (epoch,))
    row = cursor.fetchone()

    if row is None:

        cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (epoch, stake, 'HOLD', 1))
        conn.commit()

    conn.close()

def get_current_epoch():

    conn = sql.connect('SolanaStake.db')
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(epoch) FROM history")
    row = cursor.fetchone()

    conn.close()

    return row[0]

def get_most_recent_stake():
    conn = sql.connect('SolanaStake.db')
    cursor = conn.cursor()

    cursor.execute("SELECT activated_stake FROM history ORDER BY epoch DESC LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    return row[0]


def update_table(buy_sell_hold, epoch, stake, random_id):

    conn = sql.connect('SolanaStake.db')

    cursor = conn.cursor()

    #If buy 
    if buy_sell_hold == 'buy':
        cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (epoch, stake, 'BUY', random_id))
        conn.commit()

    elif buy_sell_hold == 'sell':
        cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (epoch, stake, 'SELL', random_id))
        conn.commit()

    #If hold
    else:
        cursor.execute("INSERT INTO history VALUES (?, ?, ?, ?)", (epoch, stake, 'HOLD', random_id))
        conn.commit()

    conn.close()

    return random_id
