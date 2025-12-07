from app.models import SolicitudDonante, Agendamiento, Usuario, Donante
from datetime import date, datetime
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
# Función auxiliar para calcular la edad
def calcular_edad(fecha_nacimiento):
    """Calcula la edad a partir de la fecha de nacimiento."""
    hoy = date.today()
    # Restamos el año de nacimiento al año actual.
    # Restamos 1 si la fecha de cumpleaños todavía no ha llegado este año.
    return hoy.year - fecha_nacimiento.year - (
        (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
from datetime import date
# Asegúrate de tener db, Agendamiento, Donante, Usuario importados

def obtener_agendamientos_dia():
    hoy = date.today()

    # Consulta simple (sin joinedload)
    agendamientos = (
        Agendamiento.query
        .filter(db.func.date(Agendamiento.fecha_turno) == hoy)
        .order_by(Agendamiento.fecha_turno.asc())
        .all()
    )

    resultado = []
    for ag in agendamientos:
        donante_obj = ag.donante
        usuario_donante = donante_obj.usuario

        # 1. Determinar el nombre completo del Receptor
        nombre_completo_receptor = "—" 
        if ag.receptor and ag.receptor.usuario:
            usuario_receptor = ag.receptor.usuario
            nombre_completo_receptor = f"{usuario_receptor.nombre} {usuario_receptor.apellido}"

        # 2. Construir el resultado con solo los campos esenciales
        resultado.append({
            "id_donante": ag.id_donante,
            "id_agendamiento": ag.id_agendamiento,
            "nombre_completo_donante": f"{usuario_donante.nombre} {usuario_donante.apellido}",
            "tipo_sangre": donante_obj.tipo_sangre,
            "fecha_agendamiento": ag.fecha_turno.strftime("%d/%m/%Y %H:%M"),
            "nombre_completo_receptor": nombre_completo_receptor,
        })

    return resultado

def obtener_registros_completados():
    agendamientos = (
        Agendamiento.query
        .filter(Agendamiento.estado == "completado")
        .order_by(Agendamiento.fecha_turno.desc())
        .all()
    )
    
    resultado = []
    for ag in agendamientos:
        donante_obj = ag.donante
        usuario_donante = donante_obj.usuario

        # 1. Determinar el nombre completo del Receptor
        nombre_completo_receptor = "—" 
        if ag.receptor and ag.receptor.usuario:
            usuario_receptor = ag.receptor.usuario
            nombre_completo_receptor = f"{usuario_receptor.nombre} {usuario_receptor.apellido}"

        # 2. Construir el resultado con solo los campos esenciales
        resultado.append({
            "id_donante": ag.id_donante,
            "id_agendamiento": ag.id_agendamiento,
            "nombre_completo_donante": f"{usuario_donante.nombre} {usuario_donante.apellido}",
            "tipo_sangre": donante_obj.tipo_sangre,
            "fecha_agendamiento": ag.fecha_turno.strftime("%d/%m/%Y %H:%M"),
            "nombre_completo_receptor": nombre_completo_receptor,
            "estado_agendamiento": ag.estado
        })

    return resultado

def obtener_agendamiento(id_agendamiento):

    agendamiento = Agendamiento.query.get(id_agendamiento)
    
    if not agendamiento:
        raise Exception(f"Agendamiento con ID {id_agendamiento} no encontrado.")
    
    # Acceso a las relaciones
    donante = agendamiento.donante
    usuario = donante.usuario
    
    # Calcula la edad (asumiendo que tienes la función calcular_edad)
    try:
        edad = calcular_edad(donante.fecha_nacimiento)
    except NameError:
        # Manejo si la función auxiliar no está definida, aunque lo ideal es definirla.
        edad = "Desconocida" 

    # Construye el diccionario con la información solicitada
    datos_donante = {
        "id_donante": donante.id_donante,
        "id_agendamiento": agendamiento.id_agendamiento, # Incluir el ID del agendamiento para el formulario
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "ultima_donacion": donante.ultima_donacion.strftime("%d/%m/%Y") if donante.ultima_donacion else "No registra",
        "disponible_para_donar": donante.disponible_para_donar,
        "direccion": donante.direccion,
        "tipo_sangre": donante.tipo_sangre,
        "edad": edad # Incluimos la edad calculada
    }
    
    return datos_donante # Retornamos un diccionario listo para usar en la plantilla

# En tu donaciones_controller.py
def guardar_evaluacion(id_agendamiento, resultado, comentarios, peso, temperatura, hemoglobina, presion):
    agendamiento = Agendamiento.query.get(id_agendamiento)
    if not agendamiento:
        raise Exception("El agendamiento no existe")    
    # ❗ CORRECCIÓN CLAVE: Asignar todos los signos vitales (pueden ser None si el resultado fue 'no_apto')
    agendamiento.peso = peso
    agendamiento.temperatura = temperatura
    agendamiento.hemoglobina = hemoglobina
    agendamiento.presion_arterial = presion
    agendamiento.observaciones = comentarios

    # ... (resto de la lógica de actualización del estado y donante se mantiene igual)
    if resultado == "apto":
        agendamiento.estado = 'completado'
        donante = agendamiento.donante
        donante.ultima_donacion = date.today()
        donante.disponible_para_donar = False
    elif resultado == 'no_apto':
        agendamiento.estado = 'rechazado'

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

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

def login_usuario(email, contrasena):

    usuario = Usuario.query.filter_by(email=email).first()

    # implementar check_password_hash
    if not usuario or usuario.contrasena != contrasena:
        return None

    return usuario
