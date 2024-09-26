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
    for path in PATHS_AUTORIZADOS:
      evalua_exacto =  path.count('/') == 1
      path_publico = self.header.get('X-Forwarded-Path').strip()
      
      if path_publico is not None and (path_publico == path if evalua_exacto else path_publico.startswith(path)):
        bandera = bandera + 1
      #current_app.logger.info("path_publico:%s-%s(%s)", path_publico, path, bandera)

      if self.path_local == path if evalua_exacto else self.path_local.strip().startswith(path):
        bandera = bandera + 1
      #current_app.logger.info("path_privado:%s-%s(%s)", self.path_local, path, bandera)
    
    if permitidos != bandera:
      raise IntervencionUsuario