import requests
import env
import json
from users import users


def join_policy_time():
    user = users[0]
    response = requests.post(f'{env.host}/joinpolicytest', json=user)
    data = response.json()
    # print(json.dumps(data, indent=4))
    if data['status']:
        print(f"Joining policy elapsed time - {round(data['elapsed_time'],2)} seconds")

def payout_time():
    user = users[1]
    microcontroller_data = {
        "temperature": 60,
        "humidity": 80,
        "soil_moisture": 1,
        "farm": "Puma Farm",
        "crop": "maize",
        "wallet": user['wallet'],
        "passphrase": user['passphrase']
    }
    response = requests.post(f'{env.host}/payouttest', json=microcontroller_data)
    data = response.json()
    # print(json.dumps(data, indent=2))
    if data['status']:
        print(f"Payout elapsed time - {round(data['elapsed_time'],2)} seconds")


join_policy_time()
payout_time()