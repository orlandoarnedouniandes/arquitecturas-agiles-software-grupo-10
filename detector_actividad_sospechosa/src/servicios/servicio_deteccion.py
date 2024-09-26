from datetime import datetime, timedelta

from src.enums.RazonEnum import RazonEnum
from src.models.model import InfoPublicar
from src.db.db_session import get_db


def determinar_razon(usuario_id):
    with get_db() as session:
        one_minute_ago = datetime.utcnow() - timedelta(minutes=1)
        recent_logs = session.query(InfoPublicar).filter(
            InfoPublicar.usuario_id == usuario_id,
            InfoPublicar.event_datetime >= one_minute_ago
        ).all()

        if not recent_logs:
            return None

        if len(recent_logs) < 3:
            return None

        total_logs = len(recent_logs)
        spam_logs = [log for log in recent_logs if log.path_local == "/users/autentica" and log.status_code != "200"]
        abuse_logs = [log for log in recent_logs if log.path_local == "/users/autoriza" and log.status_code != "200"]

        if len(spam_logs) / total_logs > 0.8:
            return RazonEnum.SPAM
        elif len(abuse_logs) / total_logs > 0.8:
            return RazonEnum.ABUSE

        return None