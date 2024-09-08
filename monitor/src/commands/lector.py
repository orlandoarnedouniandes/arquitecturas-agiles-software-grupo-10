from .base_command import BaseCommannd
from flask import current_app
import redis
import threading
import json
from ..validations import formato_iso_from_string
from ..models import db, Metricas, MetricasSchema
import uuid

class Lector(BaseCommannd):
  def __init__(self,host,port,bd,channel):
    self.host = host.strip()
    self.port = int(port.strip())
    self.bd = int(bd.strip())
    self.channel = channel.strip()

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
            procesador = threading.Thread(target=DatosABD(message['data'].decode('utf-8')).execute(), args=('',))
            procesador.start()

class DatosABD(BaseCommannd):
  def __init__(self,mensaje):
     self.mensaje = mensaje

  def execute(self):
    info = json.loads(self.mensaje)
    inicio = formato_iso_from_string(info.get("tiempo_inicial"))
    fin = formato_iso_from_string(info.get("tiempo_final"))
    codigo = info.get("codigo")
    latencia = (fin-inicio).total_seconds()
    current_app.logger.info(f"inicio: {inicio}, final: {fin}, codigo: {codigo}, latencia: {latencia}")
    nueva_metrica = Metricas(id=str(uuid.uuid4()), inicio=inicio, fin=fin,latencia=latencia, codigo=codigo)
    db.session.add(nueva_metrica)
    db.session.commit()
