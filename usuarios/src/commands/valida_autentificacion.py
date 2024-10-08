from .base_command import BaseCommannd
from ..errors.errors import  ExpiredInformation, Bloqued
from ..models import  Usuario, UsuarioSchema
from datetime import datetime
from flask import current_app 

    
usuario_schema = UsuarioSchema()
    
class ValidaAutentificacion(BaseCommannd):
  def __init__(self, header):
    self.header = header
    self.token = header['Authorization'].replace("Bearer ", "")
  
  def execute(self):
    usuario = Usuario.query.filter(Usuario.token == self.token).first()
    current_app.logger.info(f"usuario a validar: {usuario_schema.dump(usuario)}")
    if usuario is not None:
        if(usuario.expireAt is not None and usuario.expireAt > datetime.utcnow() and usuario.status == "VERIFICADO"):
            return usuario_schema.dump(usuario)
        if(usuario.status == 'BLOQUEADO'):
          raise Bloqued
    raise ExpiredInformation