from .base_command import BaseCommannd
from ..errors.errors import ResourcesRequired, NotFound,ToVerify, NotVerified, Bloqued
from ..models import  db, Usuario, UsuarioSchema
from ..validations import validate_empty, obtener_password
from datetime import datetime, timedelta
import hashlib
import secrets

    
usuario_schema = UsuarioSchema()
    
class Autentificar(BaseCommannd):
  def __init__(self, username, password):
    self.username = username
    self.password = password
  
  def execute(self):
    if validate_empty(self.username) or validate_empty(self.password):
        raise ResourcesRequired
    usuario = Usuario.query.filter(Usuario.username == self.username).first()
    if usuario is not None:
        if(usuario.password != hashlib.sha256(obtener_password(self.password, usuario.email).encode()).hexdigest()):
            raise NotFound
        if usuario.status == "POR_VERIFICAR":
           raise ToVerify
        if usuario.status == "NO_VERIFICADO":
           raise NotVerified
        if usuario.status == "BLOQUEADO":
           raise Bloqued
        salt = secrets.token_hex(8)
        password_salt = usuario.password + salt
        token = hashlib.sha256(password_salt.encode()).hexdigest()
        usuario.salt = salt
        usuario.token = token
        usuario.expireAt = datetime.utcnow() + timedelta(hours=3)
        usuario.updateAt = datetime.utcnow()
        db.session.commit()
        return usuario_schema.dump(usuario)
    else:
        raise NotFound