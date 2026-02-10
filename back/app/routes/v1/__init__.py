from .auth import auth_bp
from .categories import category_bp
from .technicians import technicians_bp

#Creamos una funcion que las junte y registre todos los Blueprints para que forman los endpoints de la API REST verision 1
def register_v1_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(technicians_bp)