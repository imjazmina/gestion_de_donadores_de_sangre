from app.models import SolicitudDonante, Agendamiento
from datetime import datetime
from app import db


def obtener_todas():
    solicitudes = SolicitudDonante.query.all()
    return [
        {
            "id_solicitud": s.id_solicitud,
            "id_doctor": s.id_doctor,
            "tipo_sangre": s.tipo_sangre,
            "cantidad": s.cantidad,
            "fecha_solicitud": s.fecha_solicitud,
            "estado": s.estado,
            "comentarios": s.comentarios
        }
        for s in solicitudes
    ]

def crear_turno(id_donante, fecha, hora):
    try:
        # Combinar fecha y hora en un solo datetime
        fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

        nuevo_turno = Agendamiento(
            id_donante=id_donante,
            fecha_turno=fecha_hora,
            estado='pendiente'
        )

        db.session.add(nuevo_turno)
        db.session.commit()

        return {
            "mensaje": "Turno agendado correctamente",
            "id_agendamiento": nuevo_turno.id_agendamiento,
            "fecha_turno": nuevo_turno.fecha_turno.strftime("%Y-%m-%d %H:%M"),
            "estado": nuevo_turno.estado
        }

    except Exception as e:
        db.session.rollback()
        raise e
