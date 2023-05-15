from locust import HttpUser, task, between
import env


class TestUser(HttpUser):
    wait_time = between(1, 5)
    host = env.host

    @task(1)
    def index(self):
        self.client.get("/login")

    @task(2)
    def farm_data(self):
        self.client.get("/farmdata?farm=puma")
