import requests

def computeActiveStake():

    # Compute the total number of Solana staked on mainnet

    endpoint = 'https://api.mainnet-beta.solana.com'
    headers = {'Content-Type': 'application/json',}
    json_data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getVoteAccounts',
        'params': [
            {
                'commitment': 'finalized',
            },
        ],
    }

    response = requests.post(endpoint, headers=headers, json=json_data)

    data = response.json()['result']['current']

    total = 0

    for i in range(len(data)):

        total += float(data[i]['activatedStake'])/1000000000

    return total

def determineEpochInfo():

    # Compute the current epoch and the time remaining in the epoch

    endpoint = 'https://api.mainnet-beta.solana.com'
    headers = {'Content-Type': 'application/json',}
    json_data = {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'getEpochInfo',
        'params': [
            {
                'commitment': 'finalized',
            },
        ],
    }

    response = requests.post(endpoint, headers=headers, json=json_data)

    data = response.json()['result']

    epoch = data['epoch']

    remaining_slots = data['slotsInEpoch'] - data['slotIndex']

    time_remaining_in_seconds = remaining_slots * 0.4

    time_remaining_in_hours = time_remaining_in_seconds / 60 / 60

    return (epoch, time_remaining_in_hours)

print(computeActiveStake())