from operator import or_
from app.models import SolicitudDonante, Agendamiento, Usuario, Donante, Doctor
from datetime import date, datetime
from app import db
from werkzeug.security import generate_password_hash
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from datetime import datetime
import os
from flask import current_app

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

def obtener_solicitudes():
    solicitudes = (
        db.session.query(SolicitudDonante)
        .join(Donante, SolicitudDonante.id_donante == Donante.id_donante)
        .join(Usuario, Donante.id_usuario == Usuario.id_usuario)
        .filter(SolicitudDonante.estado == 'pendiente')
        .all()
    )

    resultado = []
    for s in solicitudes:
        resultado.append({
            "id_solicitud": s.id_solicitud,
            "id_donante": s.id_donante,#este id es del donante que solicita la sangre
            "nombre": s.donante.usuario.nombre,
            "apellido": s.donante.usuario.apellido,
            "tipo_sangre": s.tipo_sangre,
            "cantidad": s.cantidad,
            "fecha_solicitud": s.fecha_solicitud.strftime("%d/%m/%Y"),
            "motivo": s.motivo,
            "estado": s.estado,
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
    
def aprobar_solicitud(id_solicitud):
    solicitud = SolicitudDonante.query.get(id_solicitud)
    if not solicitud:
        raise Exception("Solicitud no encontrada")

    solicitud.estado = 'aprobado'
    db.session.commit()

    return {
        "mensaje": "Solicitud aprobada correctamente",
        "id_solicitud": solicitud.id_solicitud,
        "estado": solicitud.estado
    }

def rechazar_solicitud(id_solicitud):
    solicitud = SolicitudDonante.query.get(id_solicitud)
    if not solicitud:
        raise Exception("Solicitud no encontrada")

    solicitud.estado = 'rechazado'
    db.session.commit()

    return {
        "mensaje": "Solicitud rechazada correctamente",
        "id_solicitud": solicitud.id_solicitud,
        "estado": solicitud.estado
    }

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
            .filter(or_(
            Agendamiento.estado == "completado",
            Agendamiento.estado == "rechazado"
    ))
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
        "estado": agendamiento.estado,
        "direccion": donante.direccion,
        "tipo_sangre": donante.tipo_sangre,
        "edad": edad # Incluimos la edad calculada
    }
    
    return datos_donante # Retornamos un diccionario listo para usar en la plantilla

def obtener_registro_agendamiento(id_agendamiento):

    ag = Agendamiento.query.get(id_agendamiento)
    
    if not ag:
        raise Exception(f"Agendamiento con ID {id_agendamiento} no encontrado.")
    
    donante = ag.donante
    usuario = donante.usuario

    # ===============================
    # 1. Determinar nombre completo del receptor 
    # ===============================
    nombre_completo_receptor = "—"

    if ag.receptor and ag.receptor.usuario:
        nombre_completo_receptor = (
            f"{ag.receptor.usuario.nombre} {ag.receptor.usuario.apellido}"
        )

    # Cálculo de edad
    try:
        edad = calcular_edad(donante.fecha_nacimiento)
    except NameError:
        edad = "Desconocida"

    datos_agendamiento = {
        "id_agendamiento": ag.id_agendamiento,
        "id_donante": donante.id_donante,

        # Donante
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "telefono": usuario.telefono,
        "direccion": donante.direccion,
        "tipo_sangre": donante.tipo_sangre,
        "edad": edad,
        "ultima_donacion": donante.ultima_donacion.strftime("%d/%m/%Y") if donante.ultima_donacion else "No registra",
        "disponible_para_donar": donante.disponible_para_donar,

        # Estado del agendamiento
        "estado": ag.estado,
        "observaciones": ag.observaciones,

        # Datos clínicos
        "peso": float(ag.peso) if ag.peso is not None else None,
        "temperatura": float(ag.temperatura) if ag.temperatura is not None else None,
        "hemoglobina": float(ag.hemoglobina) if ag.hemoglobina is not None else None,
        "presion_arterial": ag.presion_arterial,

        # Receptor
        "id_receptor": ag.id_receptor,
        "receptor_nombre_completo": nombre_completo_receptor
    }

    return datos_agendamiento


# En tu donaciones_controller.py
def guardar_evaluacion(id_agendamiento, resultado, comentarios, peso, temperatura, hemoglobina, presion):
    agendamiento = Agendamiento.query.get(id_agendamiento)
    if not agendamiento:
        raise Exception("El agendamiento no existe")    

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

def generar_pdf_agendamientos():

    # Carpeta destino
    ruta_carpeta = os.path.join(current_app.root_path, "static", "pdf")
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    ruta_archivo = os.path.join(ruta_carpeta, "registros_agendamientos.pdf")
    # Obtener registros
    agendamientos = (
        Agendamiento.query
            .filter(or_(
            Agendamiento.estado == "completado",
            Agendamiento.estado == "rechazado"
    ))
        .all()
    )

    styles = getSampleStyleSheet()
    titulo = Paragraph("Reporte de Agendamientos de Donación", styles["Title"])
    fecha_gen = Paragraph(f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles["Normal"])

    # Encabezados exactos solicitados
    tabla_data = [
        [
            "Donante",
            "Teléfono",
            "Dirección",
            "Tipo Sangre",
            "Edad",
            "Receptor",
            "Fecha Turno",
            "Estado",
            "Peso (kg)",
            "Temp (°C)",
            "Hemoglobina",
            "Presión"
        ]
    ]

    for ag in agendamientos:

        # === DONANTE ===
        don = ag.donante
        user_don = don.usuario

        nombre_donante = f"{user_don.nombre} {user_don.apellido}"
        telefono = user_don.telefono or "—"
        direccion = don.direccion or "—"
        tipo_sangre = don.tipo_sangre
        try:
            edad = calcular_edad(don.fecha_nacimiento)
        except:
            edad = "—"

        # === RECEPTOR ===
        if ag.receptor and ag.receptor.usuario:
            ur = ag.receptor.usuario
            nombre_receptor = f"{ur.nombre} {ur.apellido}"
        else:
            nombre_receptor = "—"

        # === FECHA ===
        fecha_turno = ag.fecha_turno.strftime("%d/%m/%Y %H:%M")

        # === DATOS CLÍNICOS ===
        peso = str(ag.peso) if ag.peso else "—"
        temperatura = str(ag.temperatura) if ag.temperatura else "—"
        hemoglobina = str(ag.hemoglobina) if ag.hemoglobina else "—"
        presion = ag.presion_arterial if ag.presion_arterial else "—"

        tabla_data.append([
            nombre_donante,
            telefono,
            direccion,
            tipo_sangre,
            edad,
            nombre_receptor,
            fecha_turno,
            ag.estado,
            peso,
            temperatura,
            hemoglobina,
            presion
        ])

    # Crear PDF
    doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
    elementos = [titulo, fecha_gen, Spacer(1, 20)]

    tabla = Table(tabla_data, repeatRows=1)

    # Estilos visuales
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.6, colors.grey),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('FONTSIZE', (0,0), (-1,-1), 9),
    ]))

    elementos.append(tabla)
    doc.build(elementos)

    return ruta_archivo


def obtener_donantes():
    donantes = (
        db.session.query(Donante)
        .join(Usuario, Donante.id_usuario == Usuario.id_usuario)
        .filter(Usuario.rol == 'donante')
        .all()
    )

    resultado = []
    for d in donantes:
        resultado.append({
            "id_donante": d.id_donante,
            "tipo_sangre": d.tipo_sangre,
            "nombre": d.usuario.nombre,
            "apellido": d.usuario.apellido,
            "ultima_donacion": d.ultima_donacion.strftime("%d/%m/%Y") if d.ultima_donacion else "No registra",
            "disponible_para_donar": d.disponible_para_donar,
            "direccion": d.direccion,
            "telefono": d.usuario.telefono
        })

    return resultado

def obtener_doctores():
    doctores = (
        db.session.query(Doctor)
        .join(Usuario, Doctor.id_usuario == Usuario.id_usuario)
        .filter(Usuario.rol == "doctor")
        .filter(Usuario.activo == True)
        .all()
    )

    resultado = []
    for d in doctores:
        resultado.append({
            "id_doctor": d.id_doctor,
            "nombre": d.usuario.nombre,
            "apellido": d.usuario.apellido,
            "email": d.usuario.email,
            "telefono": d.usuario.telefono,
            "especialidad": d.especialidad,
            "matricula": d.matricula,
        })

    return resultado

def obtener_doctor(id_doctor):
    d = (
        db.session.query(Doctor)
        .join(Usuario, Doctor.id_usuario == Usuario.id_usuario)
        .filter(Doctor.id_doctor == id_doctor)
        .filter(Usuario.rol == "doctor")
        .filter(Usuario.activo == True)
        .first()
    )

    if not d:
        return None

    return {
        "id_doctor": d.id_doctor,
        "nombre": d.usuario.nombre,
        "apellido": d.usuario.apellido,
        "correo": d.usuario.email,
        "telefono": d.usuario.telefono,
        "especialidad": d.especialidad
    }


def eliminar_doctor(id_doctor):
    doctor = Doctor.query.get(id_doctor)
    if not doctor:
        return False

    usuario = doctor.usuario
    usuario.activo = False  # borrado lógico

    db.session.commit()
    return True


def actualizar_doctor(id_doctor, nombre, apellido, correo, telefono, especialidad):
    doctor = Doctor.query.get(id_doctor)
    if not doctor:
        return False

    usuario = doctor.usuario
    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.email = correo
    usuario.telefono = telefono
    doctor.especialidad = especialidad

    db.session.commit()
    return True

def crear_doctor(nombre, apellido, email, telefono, contrasena, especialidad, matricula):

    # Verificar si ya existe un usuario con ese email
    if Usuario.query.filter_by(email=email).first():
        return False

    # Crear usuario base
    usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        email=email,
        telefono=telefono,
        contrasena=contrasena,
        rol="doctor",
        activo=True
    )
    db.session.add(usuario)
    db.session.commit()  # para obtener el id_usuario

    # Crear doctor vinculado
    doctor = Doctor(
        id_usuario=usuario.id_usuario,
        especialidad=especialidad,
        matricula=matricula,
    )

    db.session.add(doctor)
    db.session.commit()

    return doctor


def login_usuario(email, contrasena):

    usuario = Usuario.query.filter_by(email=email).first()

    # implementar check_password_hash
    if not usuario or usuario.contrasena != contrasena:
        return None

    return usuario
