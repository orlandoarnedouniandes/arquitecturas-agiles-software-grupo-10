from sqlalchemy import Column, String, Text, DateTime, create_engine, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from src.enums.RazonEnum import RazonEnum

Base = declarative_base()

class InfoPublicar(Base):
    __tablename__ = 'log_actividad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status_code = Column(String(10), nullable=False)
    path_local = Column(String(70), nullable=False)
    contenido = Column(Text, nullable=False)
    usuario_id = Column(String(200), nullable=False)
    ip_remota = Column(String(50), nullable=False)
    host_remoto = Column(String(100), nullable=False)
    path_remoto = Column(String(70), nullable=False)
    event_datetime = Column(DateTime, default=datetime.utcnow, nullable=False)

class UsuariosSospechosos(Base):
    __tablename__ = 'usuarios_sospechosos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(String(200), nullable=False)
    razon = Column(Enum(RazonEnum, values_callable=lambda x: [e.value for e in x]), nullable=False)
    fecha_detectado = Column(DateTime, default=datetime.utcnow, nullable=False)