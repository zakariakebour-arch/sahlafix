from flask import Flask
from app.extensions import db
from app.routes.v1 import register_v1_routes

def create_app():
    app = Flask(__name__)

    # Registrar rutas V1
    register_v1_routes(app)

    return app
