
from ..models import Solicitudes, SolicitudesSchema
from datetime import datetime, timedelta
from faker import Faker
from flask import jsonify

fake = Faker(['es_CO'])

solicitudes_Schema = SolicitudesSchema()

class ConsultaSolicitudes:
    def __init__(self, id):
        self.id = id
        self.solicitud1 = Solicitudes(
            id=fake.uuid4(),
            cliente_id=id,
            status="Pendiente",
            expireAt=fake.date_time_between(start_date="now", end_date="+30d"),
            createdAt=datetime.now(),
            updateAt=datetime.now(),
            descripcion=fake.text(max_nb_chars=200)
        )
        self.solicitud1 = solicitudes_Schema.dump(self.solicitud1)

        self.solicitud2 = Solicitudes(
            id=fake.uuid4(),
            cliente_id=fake.uuid4(),
            status="Pendiente",
            expireAt=fake.date_time_between(start_date="now", end_date="+30d"),
            createdAt=datetime.now(),
            updateAt=datetime.now(),
            descripcion=fake.text(max_nb_chars=200)
        )
        self.solicitud2 = solicitudes_Schema.dump(self.solicitud2)

    def execute(self):
        return jsonify([self.solicitud1,self.solicitud2])