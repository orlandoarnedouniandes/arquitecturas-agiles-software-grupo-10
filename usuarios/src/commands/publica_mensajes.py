from .base_command import BaseCommannd
import os
import redis
import json
from flask import current_app
from .valida_autentificacion import ValidaAutentificacion

REDIS_CHANNEL=os.environ.get("REDIS_CHANNEL")

def redis_client():
    REDIS_HOST=os.environ.get("REDIS_HOST")
    REDIS_PORT=os.environ.get("REDIS_PORT")
    REDIS_BD=os.environ.get("REDIS_BD")
    return redis.StrictRedis(host=REDIS_HOST, port= int(REDIS_PORT.strip()), db = int(REDIS_BD.strip()))

class PublicarMensajes(BaseCommannd):
    def __init__(self, header, informacion):
        self.header = header
        self.status_code = informacion.get('status_code')
        self.path_local = informacion.get('path_local')
        self.contenido = informacion.get('contenido')
        self.solicitud = informacion.get('solicitud')
        self.method = informacion.get('method')

    def execute(self):
        usuario_id = ""
        ip_remota = ""
        host_remoto = ""
        path_remoto = ""
        try:
            if 'Authorization' in self.header:
                datos_usuario = ValidaAutentificacion(self.header).execute()
                usuario_id = datos_usuario.get("id")
            if usuario_id == "" and (self.path_local in {"/users/autentica","/users"}) and self.method == "POST":
                usuario_id = json.loads(self.contenido).get("id")
        except Exception as e:
            current_app.logger.error("Error consiguiendo datos de usuario: %s", e)
        
        try:
            if 'X-Forwarded-For' in self.header:
                ip_remota = self.header.get('X-Forwarded-For')
                host_remoto = self.header.get('X-Forwarded-Host')
                path_remoto = self.header.get('X-Forwarded-Path')
        except Exception as e:
            current_app.logger.error("Error Extrayendo informacion del gateway: %s", e)

        try:
            infoPublicar = {
                "status_code": self.status_code,
                "path-local": self.path_local,
                "contenido": str(self.contenido),
                "usuario_id": usuario_id,
                "ip_remota": ip_remota,
                "host_remoto": host_remoto,
                "path_remoto": path_remoto,
                "method": self.method,
                "solicitud": str(self.solicitud)
            }
            current_app.logger.info("Publishing message to topic:  %s", infoPublicar)
            redis_client().publish(REDIS_CHANNEL, json.dumps(infoPublicar))
            current_app.logger.info("Message published successfully!")
        except Exception as e:
            current_app.logger.error("Exception: %s", e)