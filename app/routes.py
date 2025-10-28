from flask import Blueprint, render_template, jsonify
from app import controllers as donaciones_controller

bp = Blueprint('donaciones', __name__, url_prefix='/api/donaciones')
web_bp = Blueprint('donaciones_web', __name__, url_prefix='/donaciones')

# RUTA API
@bp.route('/', methods=['GET'])
def listar_donaciones():
    try:
        data = donaciones_controller.obtener_todas()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# RUTA PARA JINJA 
@web_bp.route('/')
def index():
    return render_template('index.html')
