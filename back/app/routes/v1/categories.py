from flask import Blueprint,request,jsonify
#Importamos la logica de negocio de categoria
from app.services.categories_service import CategoriesService
#Importamos decorador para rutas de admin
from app.utils.helpers import jwt_required,roles_required

category_bp = Blueprint("categories_v1",__name__,url_prefix="/api/v1/categories")

#Creamos la primera funcion que devuelve categorias
@category_bp.route("/",methods=["GET"])
def get_categories():
    #Usamos los datos que se reciben con el codigo de estado como resultado
    data,status = CategoriesService.get_categories()

    #Retornamos el resultado de la logica que se encarga de consultar las categorias en la base de datos
    return jsonify(data),status

#Creamos ruta para listar categoria segun su identificador
@category_bp.route("/<int:id>",methods=["GET"])
def get_category(id):
    #Creamos variable con el metodo y el parametro que recibira
    data,status = CategoriesService.get_category(id)

    #Retornamos la categoria con codigo de estado
    return jsonify(data),status

#Ruta para crear nueva categoria
@category_bp.route("/",methods=["POST"])
@jwt_required
@roles_required("admin")#Aqui despues de JWT correcto comprobamos si el rol es administrador
def create_category():
    #Creamos variable que contiene el metodo y el parametro json que recibe para la creacion
    data,status = CategoriesService.create(request.json)

    #Retornamos resultado con codigo de estado
    return jsonify(data),status

#Creamos ruta para eliminar categoria
@category_bp.route("/<int:id>",methods=["DELETE"])
@jwt_required
@roles_required("admin")
def delete_category(id):
    #Creamos variable con metodo y codigo estado importado de servicios
    data,status = CategoriesService.delete(id)

    #Retornamos mensaje de que se elimino correctamente
    return jsonify(data),status

#Ruta para actualizar la categoria
@category_bp.route("/<int:id>",methods=["PUT"])
@jwt_required
@roles_required("admin")
def update_category(id):
    #Creamos una variable del metodo importado con codigo de estado
    data,status = CategoriesService.update(id,request.json)

    #Retornamos resultado
    return jsonify(data),status