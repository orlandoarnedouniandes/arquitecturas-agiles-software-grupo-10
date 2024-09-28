from tkinter import EXCEPTION

from flask import jsonify
import json
import logging
from .base_command import BaseCommannd
from ..errors.errors import NotFound, ExpiredInformation, IncompleteRequest, TimeOut
from ..models import db, Cliente, ClienteSchema
from ..validations import validate_empty, es_correo_valido, obtener_fecha_actual
import os
from random import randint
from time import sleep
from ..redis_client.redis_client import redis_client
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

fake = Faker(['es_CO'])

cliente_schema = ClienteSchema()

 
class ConsultaUsuario(BaseCommannd):
    def __init__(self, id):
        self.time = obtener_fecha_actual()
        name = fake.name()
        nuevo_cliente = Cliente(id=id, username=name.split(" ")[0].lower(), email=fake.email(), dni=randint(1000000, 2000000000),
                                fullName=name, phoneNumber=randint(3000000000, 3999999999), createdAt=self.time, updateAt=self.time)
        self.nuevo_cliente = cliente_schema.dump(nuevo_cliente)

    def execute(self):
        self.publish_message_to_topic({"codigo": 200, "tiempo_inicial": self.time.isoformat(), "tiempo_final": obtener_fecha_actual().isoformat()})
        return self.nuevo_cliente

    def publish_message_to_topic(self, message):
        try:
            logger.info("Publishing message to topic:  %s", message)
            redis_client().publish("metrics", json.dumps(message))
            logger.info("Message published successfully!")
        except Exception as e:
            logger.error("Exception: %s", e)
