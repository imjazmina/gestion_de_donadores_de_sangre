from flask import Blueprint, jsonify, request
from app import controllers as donaciones_controller

bp = Blueprint('donaciones', __name__, url_prefix='/api/donaciones')
web_bp = Blueprint('donaciones_web', __name__, url_prefix='/donaciones')

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

