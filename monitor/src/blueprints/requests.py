from flask import jsonify, request, Blueprint
from ..commands.crear import Crear
import requests


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

def check_client_health():
    try:
        response = requests.get('http://127.0.0.1:3000/ping')
        if response.status_code == 200:
            return {"status": "healthy", "code": response.status_code}
        else:
            return {"status": "unhealthy", "code": response.status_code}
    except Exception as e:
        return {"status": "unreachable", "error": str(e)}
