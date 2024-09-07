from locust import HttpUser, TaskSet, task, between
import uuid

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    host = "http://localhost" 

    #@task
    #def ping(self):
    #   self.client.get("/clientes/ping")

    @task
    def queryuser(self):
        new_guid = str(uuid.uuid4())
        self.client.get(f"/clientes/{new_guid}")
    
