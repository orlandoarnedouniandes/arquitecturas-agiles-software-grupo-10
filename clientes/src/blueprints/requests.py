from venv import logger
from flask import jsonify, request, Blueprint, make_response
from ..commands.crear import Crear
from ..commands.consultaUsuario import ConsultaUsuario
from ..commands.consultaSolicitudes import ConsultaSolicitudes
from functools import wraps
import os
import requests

requests_blueprint = Blueprint('requests', __name__)

# Decorador para validar el token y los permisos
def token_required(required_permission=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return make_response(jsonify({'message': 'Token is missing!'}), 401)
            
            if not token.startswith('Bearer '):
                return make_response(jsonify({'message': 'Invalid token format!'}), 401)
            
            token = token[len('Bearer '):]
            
            authorization_service_host = 'http://host.docker.internal:3002'
            logger.info(f"Authorization service host: {authorization_service_host}")
            authorization_url = f"{authorization_service_host}/users/autoriza"

            logger.info(f"authorization_url: {authorization_url}'")

            response = requests.get(authorization_url, headers={'Authorization': token})
            
            logger.info(f"Authorization service response: {response.status_code}, {response.text}")
            if response.status_code == 401:
                return make_response(jsonify({'message': 'Token is invalid!'}), 401)
            elif response.status_code != 200:
                return make_response(jsonify({'message': 'Authorization service error!'}), 500)
            
            return f(*args, **kwargs)
        return decorated
    return decorator

@requests_blueprint.route('/', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("username"), json.get("email"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@requests_blueprint.route('/<string:id>', methods = ['GET'])
def home(id):
    print(f"GET /{id}")
    result = ConsultaUsuario(id).execute()
    return result, 200

@requests_blueprint.route('/solicitudes/<string:id>', methods = ['GET'])
@token_required(required_permission='solicitudes')
def solicitudes(id):
    print(f"GET /{id}")
    result = ConsultaSolicitudes(id).execute()
    return result, 200


@requests_blueprint.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200
