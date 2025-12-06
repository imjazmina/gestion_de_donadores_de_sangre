from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar DB
    db.init_app(app)

    # Registrar blueprints
    from app import routes as donaciones_web

    app.register_blueprint(donaciones_web.web_bp)

    # Probar conexión
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("✅ Conexión exitosa a la base de datos PostgreSQL")
        except Exception as e:
            print("❌ Error al conectar con la base de datos:", e)

    return app
