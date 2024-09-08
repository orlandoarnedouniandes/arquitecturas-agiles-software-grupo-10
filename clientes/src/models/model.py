from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(20))
    dni = db.Column(db.String(20))
    fullName = db.Column(db.String(70))
    status = db.Column(db.String(20), default="Alta")
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime)
    __tablename__ = 'cliente'

class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        load_instance = True
        
    id = fields.String()