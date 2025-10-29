from flask import Blueprint, render_template, jsonify, request
from app import controllers as donaciones_controller

bp = Blueprint('donaciones', __name__, url_prefix='/api/donaciones')
web_bp = Blueprint('donaciones_web', __name__, url_prefix='/donaciones')

# RUTA obtener solicitudes de donantes
@bp.route('/', methods=['GET'])
def listar_donaciones():
    try:
        data = donaciones_controller.obtener_todas()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<id>', methods = ['POST'])
def agendar_donacion(id):
    try:
        data = request.get_json()
        fecha = data.get('fecha')
        hora = data.get('hora')

        if not fecha or not hora:
            return jsonify({"error": "Se requieren la fecha y la hora"}), 400
        
        data = donaciones_controller.crear_turno(id, fecha, hora)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

        
