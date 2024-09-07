import os 
from flask import Flask, jsonify
from .blueprints.requests import requests_blueprint
from .errors.errors import ApiError
from flask_sqlalchemy import SQLAlchemy
from .models import db
import logging
#from celery import Celery

app = Flask(__name__)
#CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", 'redis://localhost:6379/0')
#CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", 'redis://localhost:6379/0')
#app.config['CELERY_BROKER_URL'] =  CELERY_BROKER_URL
#app.config['CELERY_RESULT_BACKEND'] = CELERY_RESULT_BACKEND

#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
#celery.conf.update(app.config)

app.register_blueprint(requests_blueprint)

database_uri= "sqlite:///dbclientes.db"
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.logger.setLevel(logging.INFO)
handler = logging.FileHandler('app.log')
app.logger.addHandler(handler)
app.logger.info('Inicializando aplicacion')

app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "mssg": err.description,
      "version": os.environ.get("VERSION")
    }
    return jsonify(response), err.code