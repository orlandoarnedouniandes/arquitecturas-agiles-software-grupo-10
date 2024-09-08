from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from uuid import uuid4


db = SQLAlchemy()

class Monitor(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    request = db.Column(db.String(32), nullable=False, unique=False)  # Client request or endpoint
    status = db.Column(db.String(32), nullable=False)  # Health status (healthy, unhealthy, unreachable)
    response_code = db.Column(db.Integer, nullable=True)  # HTTP status code
    error_message = db.Column(db.String(256), nullable=True)  # Error message if any
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __tablename__ = 'monitor'

class Metricas(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    inicio = db.Column(db.DateTime, nullable=False)  # Client request or endpoint
    fin = db.Column(db.DateTime, nullable=False)  # Health status (healthy, unhealthy, unreachable)
    latencia = db.Column(db.Float, nullable=False)  # HTTP status code
    codigo = db.Column(db.String(32), nullable=False)  # Error message if any
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __tablename__ = 'metricas'

class MonitorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Monitor
        load_instance = True

    id = fields.String()
    request = fields.String()
    status = fields.String()
    response_code = fields.Integer()
    error_message = fields.String()
    createdAt = fields.DateTime()
    updateAt = fields.DateTime()

class MetricasSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Metricas
        load_instance = True

def save_health_status(health_status):
    new_uuid = str(uuid4())

    monitor_entry = Monitor(
        id=new_uuid,
        request='client-service-ping',
        status=health_status.get("status"),
        response_code=health_status.get("code", None),
        error_message=health_status.get("error", None),
        createdAt=datetime.now(),
        updateAt=datetime.now()
    )

    db.session.add(monitor_entry)
    db.session.commit()
