from .base_command import BaseCommannd
from sqlalchemy import or_
from flask import current_app
from ..errors.errors import ResourcesRequired, ResourcesAlreadyExist
from ..models import  db, Usuario, UsuarioSchema
from ..validations import validate_empty, obtener_password, es_correo_valido, obtener_fecha_actual
from datetime import datetime
import hashlib
import uuid
    
usuario_schema = UsuarioSchema()
    
class Crear(BaseCommannd):
  def __init__(self, username, password, email, dni, fullName, phoneNumber):
    self.username = username
    self.password = password
    self.email = email
    self.dni = dni
    self.fullName = fullName
    self.phoneNumber = phoneNumber
  
  def execute(self):
    current_app.logger.info(f"usuario: {self.username}, pass: {self.password}, email: {self.email}")
    if validate_empty(self.username) or validate_empty(self.password) or validate_empty(self.email) or not es_correo_valido(self.email):
        raise ResourcesRequired
    usuario = Usuario.query.filter(or_(Usuario.username == self.username, Usuario.email == self.email)).first()
    if usuario is None:
        time = obtener_fecha_actual()
        nuevo_usuario = Usuario(id=str(uuid.uuid4()),username=self.username.strip(), password=hashlib.sha256(obtener_password(self.password, self.email).encode()).hexdigest(), email=self.email.strip(), dni=self.dni, fullName=self.fullName, phoneNumber=self.phoneNumber, createdAt=time, updateAt=time)
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)
    else:
        raise ResourcesAlreadyExist