from locust import HttpUser, task

import env
import users


class TestUser(HttpUser):
    # wait_time = between(1, 5)
    host = env.host

    def on_start(self):
        self.user = users.users.pop()

    @task(1)
    def transactionstest(self):
        self.client.post("/transactiontest", json=self.user )

