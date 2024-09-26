import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def revoke_access(usuario_id):
    users_service_url = os.environ.get("USERS_PATH", "http://localhost:3002")
    endpoint = f"{users_service_url}/users/revocar/{usuario_id}"
    response = requests.patch(endpoint)
    if response.status_code == 200:
        logger.info(f"Access revoked for user {usuario_id}")
    else:
        logger.error(f"Failed to revoke access for user {usuario_id}: {response.status_code}")