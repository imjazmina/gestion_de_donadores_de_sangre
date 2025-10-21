from flask import Flask
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Inicializar SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurar Flask desde las variables del .env
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos con la app
    db.init_app(app)

    # Probar conexión a la base de datos
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))  # Ejecuta una consulta simple
            print("✅ Conexión exitosa a la base de datos PostgreSQL")
        except Exception as e:
            print("❌ Error al conectar con la base de datos:", e)

    # Importar las rutas
    from app import routes
    app.register_blueprint(routes.bp)

    return app
