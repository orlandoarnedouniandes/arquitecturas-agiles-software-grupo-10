from .base_command import BaseCommannd
from ..errors.errors import ResourcesRequired
from ..models import  db, Usuario, UsuarioSchema
from ..validations import validate_empty, obtener_fecha_actual
from datetime import datetime
from flask import current_app


usuario_schema = UsuarioSchema()

estado = ['POR_VERIFICAR', 'NO_VERIFICADO', 'VERIFICADO', 'BLOQUEADO']

class Actualiza(BaseCommannd):
  def __init__(self, id, status):
    self.id = id
    self.status = status

  def execute(self):
    contador = 0
    usuario = Usuario.query.get_or_404(self.id)
    if(not validate_empty(self.status) and self.status in estado):
      contador = contador + 1
      usuario.status = self.status
      usuario.salt = 'fail'
    if(contador == 0):
        raise ResourcesRequired
    
    usuario.updateAt = obtener_fecha_actual()
    db.session.add(usuario)
    db.session.commit()
    return usuario_schema.dump(usuario)