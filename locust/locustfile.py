import os 
import uuid
from locust import HttpUser, TaskSet, task, between

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)   
    host =  os.getenv("LOCUST_TARGET_URL", 'http://kong:8000')

    #@task
    #def ping(self):
    #   self.client.get("/clientes/ping")

    @task
    def queryuser(self):
        new_guid = str(uuid.uuid4())
        self.client.get(f"/clientes/{new_guid}")
    
