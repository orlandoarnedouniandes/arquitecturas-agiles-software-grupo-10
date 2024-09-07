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

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cliente_schema = ClienteSchema()


class Consulta(BaseCommannd):
    def __init__(self, id):
        self.time = obtener_fecha_actual()
        nuevo_cliente = Cliente(id=id, username="primo".strip(), email="primo@gmail.com".strip(), dni="1045325478",
                                fullName="Primo", phoneNumber="3785842541", createdAt=self.time, updateAt=self.time)
        self.nuevo_cliente = cliente_schema.dump(nuevo_cliente)

    def execute(self):
        PORCENTAJE_OK = int(os.getenv("RES_OK", 90))
        resto = 100 - PORCENTAJE_OK
        valor_consultas_demoradas = int(resto / 2)
        porcentaje_contultas_demoradas = PORCENTAJE_OK + valor_consultas_demoradas
        numero_dinamico = randint(1, 100)
        if numero_dinamico <= PORCENTAJE_OK:
            print('it is ok')
        elif numero_dinamico > PORCENTAJE_OK and numero_dinamico <= porcentaje_contultas_demoradas:
            sleep(1.8)
        else:
            error = NotFound
            value = randint(1, 4)
            if value == 1:
                error = NotFound
            elif value == 2:
                error = ExpiredInformation
            elif value == 3:
                error = IncompleteRequest
            else:
                error = TimeOut

            self.publish_message_to_topic(
                {"codigo": error.code, "tiempo_inicial": self.time.isoformat(), "tiempo_final": obtener_fecha_actual().isoformat()})
            raise error
        self.publish_message_to_topic({"codigo": 200, "tiempo_inicial": self.time.isoformat(), "tiempo_final": obtener_fecha_actual().isoformat()})
        return self.nuevo_cliente

    def publish_message_to_topic(self, message):
        try:
            logger.info("Publishing message to topic:  %s", message)
            redis_client().publish("metrics", json.dumps(message))
            logger.info("Message published successfully!")
        except Exception as e:
            logger.error("Exception: %s", e)
