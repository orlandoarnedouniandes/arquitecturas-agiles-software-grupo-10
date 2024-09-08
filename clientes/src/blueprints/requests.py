from flask import jsonify, request, Blueprint
from ..commands.crear import Crear
from ..commands.consulta import Consulta


requests_blueprint = Blueprint('requests', __name__)

@requests_blueprint.route('/', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("username"), json.get("email"), json.get("dni"), json.get("fullName"), json.get("phoneNumber")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@requests_blueprint.route('/<string:id>', methods = ['GET'])
def home(id):
    print(f"GET /{id}")
    json = request.get_json()
    result = Consulta(id).execute()
    return jsonify({"id": id, "createdAt": result.get("createdAt")}), 200


@requests_blueprint.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200
