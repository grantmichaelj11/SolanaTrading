import coinbaseConnector
import sqlController as sql
import stakeCounter
import random
import string
import time

def initialization():

    epoch, _ = stakeCounter.determineEpochInfo()
    active_stake = stakeCounter.computeActiveStake()

    sql.initialize_database(epoch, active_stake)

def loop_bot():

    purchaser = coinbaseConnector.coinbaseConnector()

    while True:
        #Get current Epoch from db
        current_epoch = sql.get_current_epoch()
        #Check for new Epoch
        epoch, estimated_time_left = stakeCounter.determineEpochInfo()

        if epoch != current_epoch:
            
            # Retrieve Current Stake
            active_stake = stakeCounter.computeActiveStake()

            # Compare it to previous Stake
            previous_stake = sql.get_most_recent_stake()
            
            # Generate a random order id
            chars = string.ascii_letters + string.digits
            random_id = ''.join(random.choices(chars, k=8))

            # Compute stake difference
            stake_diff = active_stake - previous_stake

            # Purchase Logic
            if stake_diff > 0:
                decision = 'buy'
                buy = purchaser.buy_order_limit(random_id)
                if buy == 'HOLD':
                    decision = 'hold'

            elif stake_diff < 0:
                decision = 'sell'
                sell = purchaser.sell_order(random_id)
                if sell == 'HOLD':
                    decision = 'hold'
                    
            else:
                decision = 'hold'

            # Catalog update
            sql.update_table(decision, epoch, active_stake, random_id)

            print(
            f"Epoch {epoch} | "
            f"Active Stake: {active_stake:.2f} | "
            f"Previous Stake: {previous_stake:.2f} | "
            f"Stake Diff: {stake_diff:+.2f} | "
            f"Decision: {decision.upper()} | "
            f"Order ID: {random_id}"
        )

        # If not buying happens, wait!
        if estimated_time_left > 1:
            wait_time = estimated_time_left * 60 * 60 / 2
            hours = int(estimated_time_left)
            minutes = int((estimated_time_left - hours) * 60)

            print(f"Estimated time left: {hours}h {minutes}m")
            time.sleep(wait_time)

        # As we get close to the new epoch, check every minute for updated epoch
        else:
            time.sleep(60)


def run_bot():

    initialization()
    loop_bot()

run_bot()