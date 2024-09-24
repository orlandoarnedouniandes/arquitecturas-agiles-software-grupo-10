from flask import jsonify, request, Blueprint
from ..commands.crear import Crear
from ..commands.autentificacion import Autentificar
from ..commands.valida_autentificacion import ValidaAutentificacion
from ..commands.reset import Reset
from ..commands.actualiza import Actualiza
from ..commands.publica_mensajes import PublicarMensajes
from ..errors.errors import IncompleteRequest
import threading
import json

requests_blueprint = Blueprint('requests', __name__)

@requests_blueprint.route('/users', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("username"), json.get("password"), json.get("email"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@requests_blueprint.route('/users/autentica', methods = ['POST'])
def autentifica():
    json = request.get_json()
    result = Autentificar(json.get("username"), json.get("password")).execute()
    return jsonify({"id": result.get("id"),"token": result.get("token"), "expireAt": result.get("expireAt")}), 200

@requests_blueprint.route('/users/autoriza', methods = ['GET'])
def valida_autentificacion():
    #current_app.logger.info(f"header: {request.headers}")
    if 'Authorization' not in request.headers:
        raise IncompleteRequest
    result = ValidaAutentificacion(request.headers).execute()
    return jsonify({"id": result.get("id"),"username": result.get("username"), "email": result.get("email"), "fullName": result.get("fullName"), "dni": result.get("dni"), "phoneNumber": result.get("phoneNumber"), "status": result.get("status")}), 200

@requests_blueprint.route('/users/ping', methods = ['GET'])
def ping():
    return "pong", 200

@requests_blueprint.route('/users/reset', methods = ['POST'])
def reset():
    Reset().execute()
    return jsonify({"msg": "Todos los datos fueron eliminados"}), 200

@requests_blueprint.route('/users/revocar/<string:id>', methods = ['PATCH'])
def update(id):
    Actualiza(id, 'BLOQUEADO').execute()
    return jsonify({"msg": "el usuario ha sido actualizado"}), 200

@requests_blueprint.after_request
def after_request(response):
    procesador = threading.Thread(target=PublicarMensajes(request.headers,{"status_code": response.status_code,"contenido":"", "path actual": request.path}).execute(), args=('',))
    procesador.start()
    return response