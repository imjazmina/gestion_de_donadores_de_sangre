from app.models import SolicitudDonante, Agendamiento
from datetime import datetime
from app import db


def obtener_solicitudes():
    solicitudes = SolicitudDonante.query.filter_by(estado='aprobado').all()
    return [s.to_dict() for s in solicitudes]

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

def crear_solicitud(id_donante, tipo_sangre, cantidad, fecha_solicitud, comentarios):
    try:
        # Convertir fecha si viene como string
        if isinstance(fecha_solicitud, str):
            fecha_solicitud = datetime.fromisoformat(fecha_solicitud)

        nueva_solicitud = SolicitudDonante(
            id_donante=id_donante,
            tipo_sangre=tipo_sangre,
            cantidad=cantidad,
            fecha_solicitud=fecha_solicitud,
            estado='pendiente',
            comentarios=comentarios
        )

        db.session.add(nueva_solicitud)
        db.session.commit()

        return {
            "mensaje": "Solicitud creada correctamente",
            "id_solicitud": nueva_solicitud.id_solicitud
        }

    except Exception as e:
        db.session.rollback()
        raise e
