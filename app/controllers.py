from app.models import SolicitudDonante

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
