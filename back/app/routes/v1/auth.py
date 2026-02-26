from flask import Blueprint,request,jsonify
#Importamos user service
from app.services.user_service import UserRegister
auth_bp = Blueprint("auth_v1",__name__,url_prefix="/api/v1/auth")

#Creamos la ruta
@auth_bp.route("/register",methods=["POST"])
#Creamos la funcion de la ruta
def register():
    print("Peticion recibida")
    #creamos variable que contiene el metodo de crear usuario
    data,status = UserRegister.create_user(request.json)

    #Retornamos mensaje de resultado con codigo de estado
    return jsonify(data),status

#Creamos la ruta que tendra la funcion de inicio de sesión
@auth_bp.route("/login",methods=["POST"])
def login():
    #Creamos variable que contiene el metodo y codigo de estado
    data,status = UserRegister.login(request.json)

    #Retoramos mensaje de resultado con el codigo de estado
    return jsonify(data),status

