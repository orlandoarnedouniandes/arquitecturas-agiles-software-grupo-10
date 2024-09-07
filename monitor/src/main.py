import os
import time 
from flask import Flask, jsonify
from .blueprints.requests import requests_blueprint
from .errors.errors import ApiError
from flask_sqlalchemy import SQLAlchemy
from .models import db
import logging
from .commands.crear import Crear 
import threading 

app = Flask(__name__)
app.register_blueprint(requests_blueprint)

database_uri= "sqlite:///dbmonitor.db"
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

def delayed_health_check():
    app.logger.info("Waiting for 10 seconds before starting health check...")
    time.sleep(30) 

    with app.app_context():
        app.logger.info("Starting 30-second health check...")
        Crear.check_health_by_seconds(30)


def start_health_check_thread():
    health_check_thread = threading.Thread(target=delayed_health_check)
    health_check_thread.start()

start_health_check_thread()