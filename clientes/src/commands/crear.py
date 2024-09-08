from .base_command import BaseCommannd
from sqlalchemy import or_
from ..errors.errors import ResourcesRequired, ResourcesAlreadyExist
from ..models import  db, Cliente, ClienteSchema
from ..validations import validate_empty, es_correo_valido, obtener_fecha_actual
from datetime import datetime
import hashlib
import uuid
    
cliente_schema = ClienteSchema()
    
class Crear(BaseCommannd):
  def __init__(self, username, email, dni, fullName, phoneNumber):
    self.username = username
    self.email = email
    self.dni = dni
    self.fullName = fullName
    self.phoneNumber = phoneNumber
  
  def execute(self):
    if validate_empty(self.username) or validate_empty(self.password) or validate_empty(self.email) or not es_correo_valido(self.email):
        raise ResourcesRequired
    cliente = Cliente.query.filter(or_(Cliente.username == self.username, Cliente.email == self.email)).first()
    if cliente is None:
        time = obtener_fecha_actual()
        nuevo_cliente = Cliente(id=str(uuid.uuid4()),username=self.username.strip(), email=self.email.strip(), dni=self.dni, fullName=self.fullName, phoneNumber=self.phoneNumber, createdAt=time, updateAt=time)
        db.session.add(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente)
    else:
        raise ResourcesAlreadyExist