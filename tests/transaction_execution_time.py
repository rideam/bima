import requests
import env
import json
from users import users

user = users[0]
response = requests.post(f'{env.host}/joinpolicytest', json=user)
data = response.json()
# print(json.dumps(data, indent=4))
if data['status']:
    print(f"{data['elapsed_time']} seconds")
