from flask import Blueprint,request,jsonify

auth_bp = Blueprint("auth_v1",__name__,url_prefix="/api/v1/auth")

#Creamos la ruta
@auth_bp.route("/register",methods=["POST"])
#Creamos la funcion de la ruta
def register():
    #Antes comprobamos lo que nos llega como Contet-type
    if not request.is_json:
        return jsonify({"error":"Content-Type incorrecto"}),415

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error":"Formato invalido"}),400
    
    return jsonify({"message":"Registro OK"}),200

#Creamos la ruta que tendra la funcion de inicio de sesión
@auth_bp.route("/login",methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error":"Content-Type incorrecto"}),415
    
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error":"Formato invalido"}),400
    
    return jsonify({"message":"OK"}),200

