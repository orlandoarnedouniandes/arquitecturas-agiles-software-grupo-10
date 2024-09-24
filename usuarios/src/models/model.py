from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(20))
    dni = db.Column(db.String(20))
    fullName = db.Column(db.String(70))
    password = db.Column(db.String(128), nullable=False)
    salt = db.Column(db.String(128))
    token = db.Column(db.String(128))
    status = db.Column(db.String(20), default="VERIFICADO")
    expireAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updateAt = db.Column(db.DateTime)
    __tablename__ = 'usuario'

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        
    id = fields.String()