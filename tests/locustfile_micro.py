from locust import HttpUser, task

import env
import users


class TestUser(HttpUser):
    # wait_time = between(1, 5)
    host = env.host

    def on_start(self):
        self.user = users.users.pop()


    @task
    def microcontroller_data_test(self):
        microcontroller_data = {
            "temperature": 60,
            "humidity": 80,
            "soil_moisture": 1,
            "farm": "Puma Farm",
            "crop": "maize",
            "wallet": self.user['wallet'],
            "passphrase": self.user['passphrase']
        }
        self.client.post("/weatherdatatest", json=microcontroller_data)
