from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import datetime
from .model import Monitor
from uuid import uuid4


db = SQLAlchemy()

class Monitor(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    request = db.Column(db.String(32), nullable=False, unique=True)  # Client request or endpoint
    status = db.Column(db.String(32), nullable=False)  # Health status (healthy, unhealthy, unreachable)
    response_code = db.Column(db.Integer, nullable=True)  # HTTP status code
    error_message = db.Column(db.String(256), nullable=True)  # Error message if any
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updateAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __tablename__ = 'monitor'

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

def save_health_status(health_status):
    monitor_entry = Monitor(
        id=str(uuid4()),  # Generate a unique ID
        request='client-service-ping',  # Example request, can be dynamic based on the check
        status=health_status.get("status"),
        response_code=health_status.get("code", None),
        error_message=health_status.get("error", None)
    )
    db.session.add(monitor_entry)
    db.session.commit()
