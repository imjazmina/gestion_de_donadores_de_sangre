from app.models import Usuario
from flask import Blueprint, jsonify, request, render_template
from app import controllers as donaciones_controller

web_bp = Blueprint('donaciones_web', __name__)

@web_bp.route('/')
def index():
    return render_template('index.html')

# Funcionalidades donante: obtener solicitudes de donantes aprobadas
@web_bp.route('/')
def listar_solicitudes_aprobadas():
    try:
        solicitudes = donaciones_controller.obtener_solicitudes_aprobadas()
        return render_template('index.html', solicitudes=solicitudes)   
    except Exception as e:
        return jsonify({"error": str(e)}), 500  
    
# agendar citas para donar
@web_bp.route('/agendar', methods=['GET', 'POST'])
def agendar_donacion():

    if request.method == 'GET':
        return render_template('quierodonar.html')
   
    data = request.get_json()
    id_donante = data.get('idDonante')#temporal hasta login
    fecha = data.get('fecha')
    hora = data.get('hora')
    id_solicitante = data.get('id_solicitante')  # puede ser None

    if not fecha or not hora:
        return jsonify({"error": "Se requieren la fecha y la hora"}), 400

    id_donante = 1  # Temporal hasta login
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
@web_bp.route('/solicitar-donantes/<int:id_donante>', methods=['GET', 'POST'])
def crear_solicitud_donantes(id_donante):
    if request.method == 'GET':
        return render_template('solicitar.html')
    try:
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
def listar_agendamientos():
    try:
        data = donaciones_controller.obtener_agendamientos()
        return render_template('admin.html', data=data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#cambiar estado de agendamientp de donacion confirmado/cancelar
@web_bp.route('/agendamientos/<int:id_agendamiento>', methods = ['PUT'])
def cambiar_estado_agendamiento(id_agendamiento):
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')
        observacion = data.get('observacion', None)
        id_doctor = data.get('id_doctor') 

        if nuevo_estado not in ['confirmado', 'cancelado']:
            return jsonify({"error": "El estado debe ser 'confirmado' o 'cancelado'"}), 400

        resultado = donaciones_controller.actualizar_estado_agendamiento(
            id_agendamiento, nuevo_estado, observacion, id_doctor
        )
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)})
    
#funcionalidd admin
# abm usuario
@web_bp.route('/admin', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo = donaciones_controller.crear_usuario(data)
    return jsonify(nuevo), 201

@web_bp.route('/admin', methods=['GET'])
def admin():
    usuarios = donaciones_controller.obtener_usuarios()
    return render_template('admin.html', usuarios=usuarios)

@web_bp.route('/admin/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = donaciones_controller.obtener_usuario(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario), 200

@web_bp.route('/admin/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    actualizado = donaciones_controller.actualizar_usuario(id_usuario, data)
    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(actualizado), 200

@web_bp.route('/admin/<int:id_usuario>', methods=['DELETE'])
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
        # Aquí armamos la redirección según rol
        if usuario.rol == 'admin':
            redirect_url = "/admin"
        elif usuario.rol == 'doctor':
            redirect_url = "/doctor"
        else:
            redirect_url = "/index"

        return jsonify({
            "mensaje": f"Bienvenido {usuario.rol.capitalize()}",
            "redirect": redirect_url
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
