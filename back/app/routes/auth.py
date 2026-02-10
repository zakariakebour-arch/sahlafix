from flask import Blueprint,request,jsonify

auth_bp = Blueprint("auth",__name__,url_prefix="/auth")

#Creamos la ruta
@auth_bp.route("/register",methods=["POST"])
#Creamos la funcion de la ruta
def register():
    return jsonify({"message":"Registro OK"}),200


