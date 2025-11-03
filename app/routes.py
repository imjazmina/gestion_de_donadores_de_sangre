from flask import Blueprint, jsonify, request
from app import controllers as donaciones_controller


bp = Blueprint('donaciones', __name__, url_prefix='/api/donaciones')
web_bp = Blueprint('donaciones_web', __name__, url_prefix='/donaciones')
bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')

# Funcionalidades donante: obtener solicitudes de donantes aprobadas
@bp.route('/', methods=['GET'])
def listar_solicitudes_aprobadas():
    try:
        data = donaciones_controller.obtener_solicitudes_aprobadas()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# agendar citas para donar
@bp.route('/agendar/<int:id_donante>', methods = ['POST'])#limitar cantidad de agendamientos por donante
def agendar_donacion(id_donante):
    try:
        data = request.get_json()
        fecha = data.get('fecha')
        hora = data.get('hora')

        if not fecha or not hora:
            return jsonify({"error": "Se requieren la fecha y la hora"}), 400
        
        data = donaciones_controller.crear_turno(id_donante, fecha, hora)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# solicitar donantes de sangre
@bp.route('/solicitar-donantes/<int:id_donante>', methods=['POST'])
def crear_solicitud_donantes(id_donante):
    try:
        data = request.get_json()
        tipo_sangre = data.get('tipo_sangre')
        cantidad = data.get('cantidad')
        fecha_solicitud = data.get('fecha_solicitud')
        comentarios = data.get('comentarios')
        motivo = data.get('motivo')

        if not tipo_sangre or not cantidad or not fecha_solicitud:
            return jsonify({"error": "Campos incompletos"}), 400

        respuesta = donaciones_controller.crear_solicitud(
            id_donante, tipo_sangre, cantidad, fecha_solicitud, comentarios
        )
        return jsonify(respuesta), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
#funcionalidad doctor
#visualizar solicitudes de agendamiento nombre del paciente, fecha, estado y observacion
@bp.route('/agendamientos', methods = ['GET'])
def listar_agendamientos():
    try:
        data = donaciones_controller.obtener_agendamientos()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#cambiar estado de agendamientp de donacion confirmado/cancelar
@bp.route('/agendamientos/<int:id_agendamiento>', methods = ['PUT'])
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
@bp_usuarios.route('/', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo = donaciones_controller.crear_usuario(data)
    return jsonify(nuevo), 201

@bp_usuarios.route('/', methods=['GET'])
def obtener_usuarios():
    usuarios = donaciones_controller.obtener_usuarios()
    return jsonify(usuarios), 200

@bp_usuarios.route('/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    usuario = donaciones_controller.obtener_usuario(id_usuario)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(usuario), 200

@bp_usuarios.route('/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    actualizado = donaciones_controller.actualizar_usuario(id_usuario, data)
    if not actualizado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(actualizado), 200

@bp_usuarios.route('/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    eliminado = donaciones_controller.eliminar_usuario(id_usuario)
    if not eliminado:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify({"mensaje": "Usuario desactivado correctamente"}), 200



