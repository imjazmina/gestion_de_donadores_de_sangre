from app.models import SolicitudDonante, Agendamiento, Usuario, Donante
from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash

def obtener_solicitudes_aprobadas():
    solicitudes = (
        db.session.query(SolicitudDonante)
        .join(Donante, SolicitudDonante.id_donante == Donante.id_donante)
        .join(Usuario, Donante.id_usuario == Usuario.id_usuario)
        .filter(SolicitudDonante.estado == 'aprobado')
        .all()
    )

    resultado = []
    for s in solicitudes:
        resultado.append({
            "id_solicitud": s.id_solicitud,
            "tipo_sangre": s.tipo_sangre,
            "comentarios": s.comentarios,
            "motivo": s.motivo,
            "id_donante": s.id_donante,#este id es del donante que solicita la sangre
            "nombre": s.donante.usuario.nombre,
            "apellido": s.donante.usuario.apellido
        })

    return resultado

def crear_turno(id_donante, fecha, hora, id_solicitante=None    ):
    try:
        # Combinar fecha y hora en un solo datetime
        fecha_hora = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")

        nuevo_turno = Agendamiento(
            id_donante=id_donante,
            fecha_turno=fecha_hora,
            id_receptor=id_solicitante, 
            estado='pendiente'
        )

        db.session.add(nuevo_turno)
        db.session.commit()

        return {
            "mensaje": "Turno agendado correctamente",
            "id_agendamiento": nuevo_turno.id_agendamiento,
            "id_donante": nuevo_turno.id_donante,
            "fecha_turno": nuevo_turno.fecha_turno.strftime("%Y-%m-%d %H:%M"),
            "id_receptor": nuevo_turno.id_receptor,
            "estado": nuevo_turno.estado
        }

    except Exception as e:
        db.session.rollback()
        raise e

def crear_solicitud(id_donante, tipo_sangre, cantidad, fecha_solicitud, comentarios, motivo):
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
            comentarios=comentarios,
            motivo = motivo
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

#doctores
def obtener_agendamientos():
    agendamientos = Agendamiento.query.all()
    return [
        {
        "id_agendamiento" : a.id_agendamiento,
        "nombre_paciente": f"{a.donante.usuario.nombre} {a.donante.usuario.apellido}",
        "fecha_turno": a.fecha_turno.strftime("%Y-%m-%d %H:%M"),
        "estado" : a.estado,
        "observaciones" : a.observaciones
        } 
        for a in agendamientos
    ]

def actualizar_estado_agendamiento(id_agendamiento, nuevo_estado, observacion, id_doctor):
    agendamiento = Agendamiento.query.get(id_agendamiento)

    if not agendamiento:
        return {"error": "Agendamiento no encontrado"}

    agendamiento.estado = nuevo_estado
    agendamiento.observaciones = observacion
    agendamiento.id_doctor = id_doctor  
    db.session.commit()

    return {
        "mensaje": f"Agendamiento {nuevo_estado} exitosamente",
        "id_agendamiento": agendamiento.id_agendamiento,
        "estado": agendamiento.estado,
        "observacion": agendamiento.observaciones,
        "doctor": id_doctor
    }

# admin
#abm usuarios
def crear_usuario(data):
    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        email=data.get('email'),
        contrasena=generate_password_hash(data.get('contrasena')),
        rol=data.get('rol')
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario.to_dict()

def obtener_usuarios():
    usuarios = Usuario.query.all()
    return [u.to_dict() for u in usuarios]

def obtener_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    return usuario.to_dict() if usuario else None

def actualizar_usuario(id_usuario, data):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return None

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.apellido = data.get('apellido', usuario.apellido)
    usuario.email = data.get('email', usuario.email)
    usuario.rol = data.get('rol', usuario.rol)

    if 'contrasena' in data:
        usuario.contrasena = generate_password_hash(data['contrasena'])

    db.session.commit()
    return usuario.to_dict()

def eliminar_usuario(id_usuario):
    usuario = Usuario.query.get(id_usuario)
    if not usuario:
        return None
    
    usuario.activo = False
    db.session.commit()
    return True

