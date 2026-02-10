# app/__init__.py
from flask import Flask
from app.routes.v1 import register_v1_routes

def create_app():
    app = Flask(__name__)

    # Registrar los blueprints de la versión 1
    register_v1_routes(app)

    return app
