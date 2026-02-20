from flask import Blueprint,request,jsonify
#Importamos technician_service 
from app.services.technician_service import TechnicianService
#Importamos JWT
from app.utils.helpers import jwt_required,roles_required

technicians_bp = Blueprint("technicians_v1",__name__,url_prefix="/api/v1/technicians")

technicians = ["hola","mundo"]
#Endpoint que lista todos los tecnicos disponibles
@technicians_bp.route("/",methods=["GET"])
@jwt_required
def get_technicians():
    #Variable con el metodo de servicio
    data,status = TechnicianService.get_technicians()

    #Retornamos los tecnicos
    return jsonify(data),status

#Endpoint recibe segun el id seleccionado del tecnico
@technicians_bp.route("/<int:id>",methods=["GET"])
@jwt_required
def get_technician(id):
    #Creamos variable que contiene el metodo y el estado 
    data,status = TechnicianService.get_by_id(id)

    #Retornamos los datos del tecnico y codigo de estado    
    return jsonify(data),status

#Ruta para crear nuevo tecnico
@technicians_bp.route("/",methods=["POST"])
@jwt_required
@roles_required("technician")#Para cualquier modificacion del tecnico tenemos que comprobar que es rol tecnico
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
    
    return jsonify({"message":"Archivo recibido"}),200


   