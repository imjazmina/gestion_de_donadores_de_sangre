from flask import Blueprint, jsonify, request, render_template, session, redirect, url_for, send_file
from app import controllers as donaciones_controller
from app.auth import login_required, rol_required

web_bp = Blueprint('donaciones_web', __name__)

# Funcionalidades donante: obtener solicitudes de donantes aprobadas
@web_bp.route('/')
def index():
    try:
        solicitudes = donaciones_controller.obtener_solicitudes_aprobadas()
        return render_template('index.html', solicitudes=solicitudes)   
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
# agendar citas para donar
@web_bp.route('/agendar', methods=['GET', 'POST'])
@login_required
def agendar_donacion():

    if request.method == 'GET':
        return render_template('quierodonar.html')
    data = request.get_json()
    id_donante = session.get("usuario_id")
    fecha = data.get('fecha')
    hora = data.get('hora')
    id_solicitante = data.get('id_solicitante')  # puede ser None

    if not fecha or not hora:
        return jsonify({"error": "Se requieren la fecha y la hora"}), 400

    try:
        data = donaciones_controller.crear_turno(
            id_donante=id_donante,
            fecha=fecha,
            hora=hora,
            id_solicitante=id_solicitante,   # aquí lo usás
        )

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# solicitar donantes de sangre
@web_bp.route('/solicitar-donantes', methods=['GET', 'POST'])
@login_required
def crear_solicitud_donantes():
    if request.method == 'GET':
        return render_template('solicitar.html')
    try:
        id_donante = session.get("usuario_id")
        tipo_sangre = request.form.get('tipo_sangre')
        cantidad = request.form.get('cantidad')
        fecha_solicitud = request.form.get('fecha_solicitud')
        comentarios = request.form.get('comentarios')
        motivo = request.form.get('motivo')

        if not tipo_sangre or not cantidad or not fecha_solicitud:
            return jsonify({"error": "Campos incompletos"}), 400

        respuesta = donaciones_controller.crear_solicitud(
            id_donante, tipo_sangre, cantidad, fecha_solicitud, comentarios, motivo
        )
        return jsonify(respuesta), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#funcionalidad doctor
#visualizar solicitudes de agendamiento nombre del paciente, fecha, estado y observacion

@web_bp.route('/doctor', methods=['GET'])
@rol_required('doctor')
def listar_agendamientos():
    try:
        data = donaciones_controller.obtener_agendamientos_dia()
        return render_template('admin.html', data=data,  active_page='citas')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_bp.route('/doctor/completados', methods=['GET'])
@rol_required('doctor')
def listar_agendamientos_completados():
    try:
        data = donaciones_controller.obtener_registros_completados()
        return render_template('donacionesRegistradas.html', data=data ,active_page='completados') 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Si la evaluación es por agendamiento
@web_bp.route('/evaluacion/<int:id_agendamiento>')
def mostrar_evaluacion(id_agendamiento):
    try:
    # Tendrías que obtener el agendamiento y luego el donante
        agendamiento = donaciones_controller.obtener_agendamiento(id_agendamiento)
        # Pasa el objeto completo del agendamiento a la plantilla
        return render_template('evaluacion_donante.html', agendamiento=agendamiento)
    
    except Exception as e:
        return render_template('evaluacion_donante.html', agendamiento=agendamiento )

@web_bp.route('/registro-evaluacion/<int:id_agendamiento>')
def mostrar_registro_evaluacion(id_agendamiento):
    try:
        agendamiento = donaciones_controller.obtener_registro_agendamiento(id_agendamiento)
        return render_template('registroDonacion.html', agendamiento=agendamiento)
    except Exception as e:
        return render_template('registroDonacion.html', agendamiento=agendamiento )

@web_bp.route("/pdf/agendamientos")
def descargar_pdf_agendamientos():
    archivo = donaciones_controller.generar_pdf_agendamientos()
    return send_file(archivo, as_attachment=True)

# Función auxiliar para manejar cadenas vacías y conversión segura
def safe_float(value):
    if value and value.strip():
        try:
            return float(value)
        except ValueError:
            # Capturará si el input es 'abc'
            raise ValueError("Valor numérico inválido en peso, temperatura o hemoglobina.")
    # Si está vacío, devolvemos None (NULL) o 0.0 si es mandatorio por la DB
    return None 

@web_bp.route('/evaluacion/<int:id_agendamiento>/guardar', methods=['POST'])
def guardar_evaluacion(id_agendamiento):
    try:
        # Obtener el ID del doctor logueado desde la sesión o del objeto de usuario
        # Asumiendo que guardas el ID del doctor en la sesión
        resultado = request.form.get("resultado") 
        comentarios = request.form.get("comentarios") or None # Convierte cadena vacía a None

        # Procesar datos solo si es 'apto' o si están llenos
        if resultado == 'apto':
            peso = safe_float(request.form.get("peso"))
            temperatura = safe_float(request.form.get("temperatura"))
            hemoglobina = safe_float(request.form.get("hemoglobina"))
            presion = request.form.get("presion") or None
            
        # CORRECCIÓN: Usar 'no_apto' del HTML
        elif resultado == 'no_apto': 
            peso = None
            temperatura = None
            hemoglobina = None
            presion = None
        
        # Llamar al controlador de negocio
        donaciones_controller.guardar_evaluacion(
            id_agendamiento=id_agendamiento,
            resultado=resultado,
            comentarios=comentarios,
            peso=peso,
            temperatura=temperatura,
            hemoglobina=hemoglobina,
            presion=presion
        )
        return jsonify({
            "success": True, 
            "message": "Evaluación guardada con éxito."
        }), 200 
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

#listar solicitudes de donacion pendientes de confirmar/cancelar
@web_bp.route('/solicitudes', methods = ['GET'])
def mostrar_solicitudes():
    try:
        solicitudes = donaciones_controller.obtener_solicitudes()
        return render_template('solicitudesDoctor.html', solicitudes=solicitudes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
@web_bp.route('/solicitudes/<int:id_solicitud>/aprobar', methods=['POST'])
def aprobar_solicitud(id_solicitud):
    solicitud = donaciones_controller.aprobar_solicitud(id_solicitud)
    return redirect(url_for('donaciones_web.mostrar_solicitudes', solicitud=solicitud))


@web_bp.route('/solicitudes/<int:id_solicitud>/rechazar', methods=['POST'])
def rechazar_solicitud(id_solicitud):
    solicitud = donaciones_controller.rechazar_solicitud(id_solicitud=id_solicitud)
    return redirect(url_for('donaciones_web.mostrar_solicitudes', solicitud=solicitud))

@web_bp.route('/donantes')
def listar_donantes():
    donantes = donaciones_controller.obtener_donantes()
    return render_template('donantes.html', donantes=donantes)
    
# abm usuario
@web_bp.route('/admin', methods=['POST'])
@rol_required('admin')
def crear_usuario():
    data = request.get_json()
    nuevo = donaciones_controller.crear_usuario(data)
    return jsonify(nuevo), 201

@web_bp.route('/admin/<int:id_usuario>', methods=['GET'])
@rol_required('admin')
def obtener_usuario(id_usuario):
    usuario = donaciones_controller.obtener_usuario(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario), 200

@web_bp.route('/admin/<int:id_usuario>', methods=['PUT'])
@rol_required('admin')
def actualizar_usuario(id_usuario):
    data = request.get_json()
    actualizado = donaciones_controller.actualizar_usuario(id_usuario, data)
    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(actualizado), 200

@web_bp.route('/admin/<int:id_usuario>', methods=['DELETE'])
@rol_required('admin')
def eliminar_usuario(id_usuario):
    eliminado = donaciones_controller.eliminar_usuario(id_usuario)
    if not eliminado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario desactivado correctamente"}), 200

@web_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    try:
        data = request.get_json()
        email = data.get('email')
        contrasena = data.get('contrasena')

        if not email or not contrasena:
            return jsonify({"error": "Email y contraseña requeridos"}), 400
        
        usuario = donaciones_controller.login_usuario(email, contrasena)

        if not usuario:
            return jsonify({"error": "Credenciales inválidas"}), 401
        
        # Guardamos sesión
        session['usuario_id'] = usuario.id_usuario
        session['rol'] = usuario.rol
        session['nombre'] = usuario.nombre
        session.permanent = False


        if usuario.rol == 'admin':
            redirect_url = "/admin"
        elif usuario.rol == 'doctor':
            redirect_url = "/doctor"
        else:
            redirect_url = "/"

        return jsonify({
            "mensaje": f"Bienvenido {usuario.rol.capitalize()}",
            "redirect": redirect_url
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@web_bp.route('/logout', methods=['GET'])
def logout():
    session.clear()  # opcional
    session['logout_ok'] = True  # flag temporal
    return redirect(url_for('donaciones_web.index'))

#registro de donantes

