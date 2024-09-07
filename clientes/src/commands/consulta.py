from .base_command import BaseCommannd
from ..errors.errors import NotFound, ExpiredInformation, IncompleteRequest, TimeOut
from ..models import  db, Cliente, ClienteSchema
from ..validations import validate_empty, es_correo_valido, obtener_fecha_actual
from datetime import datetime
import hashlib
import uuid
import os
from random import randint
from time import sleep
#from celery import Celery
    
cliente_schema = ClienteSchema()

# Definimos una tarea Celery
#@celery.task
#def info_request(codigo, desc,request,tiempo_entrada,tiempo_salida):
#    return {codigo,desc,request,tiempo_entrada,tiempo_salida}
    
class Consulta(BaseCommannd):
  def __init__(self, id):
    self.time = obtener_fecha_actual()
    nuevo_cliente = Cliente(id=id,username="primo".strip(), email="primo@gmail.com".strip(), dni="1045325478", fullName="Primo", phoneNumber="3785842541", createdAt=self.time , updateAt=self.time )
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
        value= randint(1, 4)
        if value == 1:
            error = NotFound
        elif value == 2:
            error = ExpiredInformation
        elif value == 3:
            error = IncompleteRequest
        else:
            error = TimeOut
        #task = info_request.apply_async(args=[error.code, error.description,"id",self.time, obtener_fecha_actual()])
        raise error
    #task = info_request.apply_async(args=[200, "","id",self.time, obtener_fecha_actual()])
    return self.nuevo_cliente
    

        
