from .base_command import BaseCommannd
from sqlalchemy import or_
from ..errors.errors import ResourcesRequired, ResourcesAlreadyExist
from ..models import  db, Monitor, MonitorSchema
from ..validations import validate_empty, es_correo_valido, obtener_fecha_actual
from datetime import datetime
import hashlib
import uuid
    
monitor_schema = MonitorSchema()
    
class Crear(BaseCommannd):
  def __init__(self, request):
    self.request = request

  
  def execute(self):
    if validate_empty(self.request) or validate_empty(self.password) or validate_empty(self.email) or not es_correo_valido(self.email):
        raise ResourcesRequired
    monitor = Monitor.query.filter(Monitor.request == self.request).first()
    if monitor is None:
        time = obtener_fecha_actual()
        nuevo_monitor = Monitor(id=str(uuid.uuid4()),request=self.request.strip(), createdAt=time, updateAt=time)
        db.session.add(nuevo_monitor)
        db.session.commit()
        return monitor_schema.dump(nuevo_monitor)
    else:
        raise ResourcesAlreadyExist