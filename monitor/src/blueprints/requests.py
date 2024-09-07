from flask import jsonify, request, Blueprint
from ..commands.crear import Crear


requests_blueprint = Blueprint('requests', __name__)

@requests_blueprint.route('/', methods = ['POST'])
def crear():
    json = request.get_json()
    result = Crear(json.get("request")).execute()
    return jsonify({"id": result.get("id"), "createdAt": result.get("createdAt")}), 201

@requests_blueprint.route('/', methods = ['GET'])
def home():
    return "Hola", 200


@requests_blueprint.route('/ping', methods = ['GET'])
def ping():
    return "pong", 200
