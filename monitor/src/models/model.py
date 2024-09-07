from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Monitor(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    request = db.Column(db.String(32), nullable=False, unique=True)
    createdAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime)
    __tablename__ = 'monitor'

class MonitorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Monitor
        load_instance = True
        
    id = fields.String()