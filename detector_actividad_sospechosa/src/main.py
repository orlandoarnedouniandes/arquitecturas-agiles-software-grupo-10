import json
import logging
import os
import threading

import redis
from datetime import datetime
from flask import Flask
from src.models import InfoPublicar, UsuariosSospechosos, Base
from src.servicios.servicio_deteccion import determinar_razon
from src.servicios.servicio_revocacion import revoke_access
from src.blueprints.endpoints import endpoint_blueprints
from src.db.db_session import get_db

REDIS_HOST=os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT=os.environ.get("REDIS_PORT", 6379)
REDIS_BD=os.environ.get("REDIS_BD", 0)
REDIS_CHANNEL=os.environ.get("REDIS_CHANNEL", "accesos")


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(endpoint_blueprints)
app.logger.setLevel(logging.INFO)
app_context = app.app_context()
app_context.push()

logger.info('Inicializando aplicacion')


redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_BD)
def process_redis_messages():
    pubsub = redis_client.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)

    while True:
        message = pubsub.get_message(ignore_subscribe_messages=True, timeout=1)
        if message is None:
            continue

        if message['type'] == 'message':
            try:
                logger.info(f"Processing message: {message}")
                data = json.loads(message['data'])
                logger.info(f"Parsed data: {data}")

                if data['usuario_id'] == "":
                    logger.info("No se puede procesar el mensaje porque no tiene usuario_id")
                    data['usuario_id'] = "unknown"

                with get_db() as session:
                    logger.info(f"Saving access logs for user {data['usuario_id']}")
                    path_local=data.get('path-local', '')
                    staus_code=data.get('status_code', '')
                    access_logs = InfoPublicar(
                        status_code=data.get('status_code', ''),
                        path_local=data.get('path-local', ''),
                        contenido=data.get('contenido', ''),
                        usuario_id=data['usuario_id'],  # Use updated usuario_id
                        ip_remota=data.get('ip_remota', ''),
                        host_remoto=data.get('host_remoto', ''),
                        path_remoto=data.get('path_remoto', '')
                    )
                    session.add(access_logs)
                    session.commit()
                    logger.info(f"Access logs saved for user {data['usuario_id']}")

                    
                    if path_local == "/users/autoriza" and staus_code != 200:
                        logger.info(f"User suspicious. Reason: {staus_code}")
                        logger.info(f"User {data['usuario_id']} is suspicious. Reason: {'Unforbidden'}")
                        usuario_sospechoso = UsuariosSospechosos(
                            usuario_id=data['usuario_id'],
                            razon='Unforbidden',
                            fecha_detectado=datetime.utcnow()
                        )
                        session.add(usuario_sospechoso)
                        session.commit()  # Commit at the end
                        revoke_access(data['usuario_id'])
                    else:
                        logger.info(f"User {data['usuario_id']} is not suspicious")
            except Exception as e:
                logger.error(f"Error processing message: {e}")


# Use a separate thread to process Redis messages
thread = threading.Thread(target=process_redis_messages)
thread.start()