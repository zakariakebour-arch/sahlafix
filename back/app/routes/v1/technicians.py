from flask import Blueprint,request,jsonify

technicians_bp = Blueprint("technicians_v1",__name__,url_prefix="/api/v1/technicians")


#Endpoint que lista todos los tecnicos disponibles
@technicians_bp.route("",methods=["GET"])
def get_technicians():
    return jsonify({"message":[]}),200

#Endpoint recibe segun el id seleccionado del tecnico
@technicians_bp.route("/<int:id>",methods=["GET"])
def get_technician(id):
    
    return jsonify({"message":""})

#Endpoint que recibe foto de perfil
@technicians_bp.route("/me/avatar",methods=["POST"])
def get_photo_profile():
    #Recibe un archivo
    file = request.files.get("file")

    return jsonify({"message":"Lo dejamos asi de momento"}),200

