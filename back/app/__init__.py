from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.routes.v1 import register_v1_routes
from app.config import Config
# Importamos los modelos para que SQLAlchemy los detecte
from app import models

def create_app():
    app = Flask(__name__)
    
    # Cargamos la configuracion de conexion a la base de datos MySQL
    app.config.from_object(Config)
    
    # Inicializamos CORS
    CORS(app)
    
    # Inicializar extensiones (SQLAlchemy)
    db.init_app(app)
    
    # Registramos los endpoints de la v1
    register_v1_routes(app)

    # Aqui creamos las tablas si no existen
    with app.app_context():
        db.create_all()
    
    # Retornamos la app completa
    return app