from .base_command import BaseCommannd
import os
import redis
import json
from flask import current_app

REDIS_CHANNEL=os.environ.get("REDIS_CHANNEL")

def redis_client():
    REDIS_HOST=os.environ.get("REDIS_HOST")
    REDIS_PORT=os.environ.get("REDIS_PORT")
    REDIS_BD=os.environ.get("REDIS_BD")
    return redis.StrictRedis(host=REDIS_HOST, port= int(REDIS_PORT.strip()), db = int(REDIS_BD.strip()))

class PublicarMensajes(BaseCommannd):
    def __init__(self, header, informacion):
        self.header = header
        self.informacion = informacion

    def execute(self):
        try:
            current_app.logger.info("Publishing message to topic:  %s, %s", self.informacion, "vacio")
            redis_client().publish(REDIS_CHANNEL, json.dumps(self.informacion))
            current_app.logger.info("Message published successfully!")
        except Exception as e:
            current_app.logger.error("Exception: %s", e)