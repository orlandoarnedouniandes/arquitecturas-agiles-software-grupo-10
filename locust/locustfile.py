import os 
import uuid
from venv import logger
from locust import HttpUser, TaskSet, task, between
from faker import Faker
import random
import json

fake = Faker()

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)   
    host =  os.getenv("LOCUST_TARGET_URL", 'http://kong:8000')
    Token = None

    @task
    def validatepermissions(self):
        self.user = self.createuser()

        if self.Token is None:
            response = self.client.post("/usuario",json=self.user)
            logger.info(f"POST to /usuario response {response} with status code {response.status_code} and response {response.text}")
            try:
                self.id = json.loads(response.text).get("id")
            except:
                self.id = None
                self.Token = None
            self.Token = self.get_token()
        else:
            logger.info(f"Id: {self.id} - Token: {self.Token}")
            urls = [
                f"/clientes/personalinfo/{self.id}",
                f"/clientes/solicitudes/{self.id}",
            ]
            probabilities = [0.7, 0.3]
            selected_url = random.choices(urls, probabilities)[0]
            headers = {'Authorization': f'Bearer {self.Token}'}
            response = self.client.get(selected_url, headers=headers)
            logger.info(f"GET to {selected_url} with status code {response.status_code} and response {response.text}")
            if response.status_code == 444:
                self.Token = None

    def get_token(self):
        response = self.client.post("/usuario/autentica", json={"username": self.username, "password": self.password})
        return response.json().get("token")

    def createuser(self):
        self.username = fake.user_name()
        self.password = fake.password()
        self.email = fake.email()
        self.dni = fake.ssn()
        self.full_name = fake.name()
        self.phone_number = fake.phone_number()

        return {
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "dni": self.dni,
            "fullName": self.full_name,
            "phoneNumber": self.phone_number
        }