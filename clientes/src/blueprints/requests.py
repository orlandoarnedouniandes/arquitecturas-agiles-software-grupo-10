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
def token_required():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            authorization_service_host = os.getenv('USERS_PATH')
            authorization_url = f"{authorization_service_host}/users/autoriza"

            logger.info(f"headers {request.headers}'")
            logger.info(f"token: Authorization {request.headers.get('Authorization')}'")

            response = requests.get(authorization_url, headers=request.headers)
            
            logger.info(f"Authorization service response: {response.status_code}, {response.text}")

            if response.status_code != 200:
                return make_response(response.text, response.status_code)
            
            return f(*args, **kwargs)
        return decorated
    return decorator

@requests_blueprint.route('/', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("username"), json.get("email"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@requests_blueprint.route('/personalinfo/<string:id>', methods = ['GET'])
@token_required()
def home(id):
    print(f"GET /{id}")
    result = ConsultaUsuario(id).execute()
    return result, 200

@requests_blueprint.route('/solicitudes/<string:id>', methods = ['GET'])
@token_required()
def solicitudes(id):
    print(f"GET /{id}")
    result = ConsultaSolicitudes(id).execute()
    return result, 200


@requests_blueprint.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200
