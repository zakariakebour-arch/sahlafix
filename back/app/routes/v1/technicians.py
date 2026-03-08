from flask import Blueprint,request,jsonify,g,current_app
#Importamos technician_service 
from app.services.technician_service import TechnicianService
#Importamos JWT
from app.utils.helpers import jwt_required,roles_required

#IMPORTACIONES NUEVAS PARA SUBIDA DE IMAGEN
from werkzeug.utils import secure_filename
import os
from app.models.technician import Technician
from app.extensions import db

technicians_bp = Blueprint("technicians_v1",__name__,url_prefix="/api/v1/technicians")

#Endpoint que lista todos los tecnicos disponibles
@technicians_bp.route("/",methods=["GET"])
def get_technicians():
    #Variable con el metodo de servicioS
    data,status = TechnicianService.get_technicians()

    #Retornamos los tecnicos
    return jsonify(data),status

#Endpoint recibe segun el id seleccionado del tecnico
@technicians_bp.route("/<int:id>",methods=["GET"])
def get_technician(id):
    #Creamos variable que contiene el metodo y el estado 
    data,status = TechnicianService.get_by_id(id)

    #Retornamos los datos del tecnico y codigo de estado    
    return jsonify(data),status

#Ruta para crear nuevo tecnico (solo admin, no se usa en registro)
@technicians_bp.route("/",methods=["POST"])
@roles_required("admin")
@jwt_required
def create_technician():
    #Creamos variable que contiene el metodo de creacion de tecnico con codigo de estado y recibe un diccionario
    data,status = TechnicianService.create_technician(request.json)

    #Retornamos el resultado
    return jsonify(data),status
 
#Endpoint que recibe foto de perfil
@technicians_bp.route("/avatar",methods=["POST"])
@jwt_required
@roles_required("technician")
def get_photo_profile():

    #Recibe un archivo
    file = request.files.get("file")

    if not file:
        return jsonify({"error":"Archivo requerido"}),400

    #Limpiamos el nombre del archivo para evitar problemas de seguridad
    filename = secure_filename(file.filename)

    #Generamos nombre unico usando el id del usuario
    unique_name = f"{g.current_user.id}_{filename}"

    #Ruta donde se guardara la imagen
    upload_folder = os.path.join(os.getcwd(), "app", "uploads", "avatars")

    #Creamos la carpeta si no existe
    os.makedirs(upload_folder, exist_ok=True)

    #Ruta completa del archivo
    upload_path = os.path.join(upload_folder, unique_name)

    #Guardamos el archivo en el sistema
    file.save(upload_path)

    #Buscamos el tecnico asociado al usuario logueado
    technician = Technician.query.filter_by(user_id=g.current_user.id).first()

    #Si no existe tecnico asociado
    if not technician:
        return jsonify({"error":"Tecnico no encontrado"}),404

    #Guardamos el nombre del archivo en la base de datos
    technician.photo_profile = unique_name

    #Guardamos cambios
    db.session.commit()

    return jsonify({
        "message":"Foto subida correctamente",
        "image": unique_name
    }),200

#Ruta para busqueda de tecnicos con el buscador
@technicians_bp.route("/search", methods=["GET"])
def buscar():
    # Obtenemos el parámetro de la query string
    name = request.args.get("name", "").strip()
    
    # Validamos que se haya pasado un valor
    if not name:
        return jsonify({"error": "Se requiere el parámetro 'name'"}), 400

    # Aqui va el enpoint que vamos a exponer para la busqueda
    data, status = TechnicianService.search_by_name(name)

    # Retornamos resultado
    return jsonify(data), status

#Metodo que recibe longitud y latitud para actualizar
@technicians_bp.route("/<int:technician_id>/location",methods=["PUT"])
@roles_required("technician")
@jwt_required
def location(technician_id):

    #Recibimos datos del body en formato JSON
    data = request.get_json()

    #Llamamos el metodo del service
    data,status = TechnicianService.location_request(technician_id,data)

    #Retornamos mensaje de resultado
    return jsonify(data),status

#Metodo para cargar la informacion actual del tecnico antes de modifcar
@technicians_bp.route("/me", methods=["GET"])
@jwt_required
@roles_required("technician")
def get_my_profile():

    user_id = g.current_user.id

    # Llamamos al service
    data, status = TechnicianService.get_by_user_id(user_id)

    return jsonify(data), status

#Endpoint para que el tecnico actualice sus datos
@technicians_bp.route("/me", methods=["PUT"])
@jwt_required
@roles_required("technician")
def update_technician():

    #Datos enviados en JSON
    data = request.get_json()

    #Usuario del token
    user_id =  g.current_user.id

    #Llamamos al service
    data, status = TechnicianService.update_technician(data, user_id)

    #Retornamos respuesta
    return jsonify(data), status