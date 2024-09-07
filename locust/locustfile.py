from locust import HttpUser, TaskSet, task, between
import uuid

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def index(self):
        self.client.get("/clientes/ping")

    @task
    def index(self):
        new_guid = str(uuid.uuid4())
        self.client.get("/clientes/{newguid}")
    
