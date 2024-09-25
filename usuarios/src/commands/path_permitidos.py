from .base_command import BaseCommannd
from flask import current_app
import os
from ..errors.errors import IntervencionUsuario

PATHS_AUTORIZADOS=os.environ.get("PATHS_AUTORIZADOS").split(",")
    
class ValidarPathPermitidos(BaseCommannd):
  def __init__(self, header, path_local):
    self.header = header
    self.path_local = path_local
  
  def execute(self):
    bandera = 0
    permitidos = 0
    if self.header.get('X-Forwarded-Path') is not None:
      permitidos = 2
    else:
      permitidos = 1
    if self.header.get('X-Forwarded-Path').strip() in PATHS_AUTORIZADOS:
      bandera = bandera + 1
    if self.path_local in PATHS_AUTORIZADOS:
      bandera = bandera + 1
    if permitidos != bandera:
      raise IntervencionUsuario