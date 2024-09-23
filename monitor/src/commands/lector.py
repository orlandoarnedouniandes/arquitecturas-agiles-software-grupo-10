from .base_command import BaseCommannd
from flask import current_app
import redis
import threading
import json
from ..validations import formato_iso_from_string
from ..models import db, Metricas, MetricasSchema
import uuid

class Lector(BaseCommannd):
  def __init__(self,host,port,bd,channel,cods_indisponibilidad, tiempo_indisponibilidad):
    self.host = host.strip()
    self.port = int(port.strip())
    self.bd = int(bd.strip())
    self.channel = channel.strip()
    self.cods_indisponibilidad = cods_indisponibilidad.split(",")
    self.tiempo_indisponibilidad = tiempo_indisponibilidad

  def execute(self):
    # Connect to Redis
    client = redis.StrictRedis(host=self.host, port=self.port, db=self.bd)
    
    # Subscribe to the specified channel
    pubsub = client.pubsub()
    pubsub.subscribe(self.channel)
    current_app.logger.info(f"Subscribed to channel: {self.channel}")

    # Listen for messages on the channel
    for message in pubsub.listen():
        if message and message['type'] == 'message':
            current_app.logger.info(f"Received message: {message['data'].decode('utf-8')} on channel: {message['channel'].decode('utf-8')}")
            procesador = threading.Thread(target=DatosABD(message['data'].decode('utf-8'), self.cods_indisponibilidad, self.tiempo_indisponibilidad).execute(), args=('',))
            procesador.start()

class DatosABD(BaseCommannd):
  def __init__(self,mensaje, cods_indisponibilidad, tiempo_indisponiblidad):
     self.mensaje = mensaje
     self.cods_indisponibilidad = cods_indisponibilidad
     self.tiempo_indisponibilidad = tiempo_indisponiblidad

  def execute(self):
    info = json.loads(self.mensaje)
    inicio = formato_iso_from_string(info.get("tiempo_inicial"))
    fin = formato_iso_from_string(info.get("tiempo_final"))
    codigo = int(info.get("codigo"))
    latencia = round((fin-inicio).total_seconds() * 1000, 2)
    current_app.logger.info(f"inicio: {inicio}, final: {fin}, codigo: {codigo}, latencia: {latencia}")
    if (latencia >= float(self.tiempo_indisponibilidad) and codigo==200) or str(codigo) in self.cods_indisponibilidad:
      nueva_metrica = Metricas(id=str(uuid.uuid4()), codigo=codigo, inicio=inicio, fin=fin, latencia=latencia)
      db.session.add(nueva_metrica)
      db.session.commit()
