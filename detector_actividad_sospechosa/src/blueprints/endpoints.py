from flask import Blueprint

endpoint_blueprints = Blueprint('endpoints', __name__)

@endpoint_blueprints.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200

@endpoint_blueprints.route('/', methods = ['GET'])
def home():
    return "DETECTOR ACTIVIDAD SOSPECHOSA", 200