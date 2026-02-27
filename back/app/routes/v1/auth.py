from flask import Blueprint,request,jsonify
#Importamos user service
from app.services.user_service import UserRegister
#Importamos technician service
from app.services.technician_service import TechnicianService

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

#Ruta para registrar técnico usuario y tecnico
@auth_bp.route("/register-technician", methods=["POST"])
def register_technician():
    data = request.json

    #Verificamos que el rol sea tecnico
    if data.get("role") != "technician":
        return jsonify({"error": "El rol debe ser technician"}), 400

    #Creamos el usuario primero
    user_data = {
        "email": data.get("email"),
        "password": data.get("password"),
        "role": "technician"
    }

    user_response, status = UserRegister.create_user(user_data)

    if status != 201:
        return jsonify(user_response), status

    new_user_id = user_response["user"]["id"]

    # Validación segura de category_id
    raw_category = data.get("category_id")

    if raw_category is None or raw_category == "":
        return jsonify({"error": "category_id es obligatorio"}), 400

    try:
        category_id = int(raw_category)
    except ValueError:
        return jsonify({"error": "category_id debe ser un número"}), 400

    #Creamos el tecnico
    technician_data = {
        "full_name": data.get("full_name"),
        "category_id": category_id,
        "wilaya": data.get("wilaya"),
        "city": data.get("city"),
        "description": data.get("description"),
        "phone": data.get("phone"),
        "user_id": new_user_id,
        "is_active": True
    }

    tech_response, tech_status = TechnicianService.create_technician(technician_data)

    if tech_status != 201:
        return jsonify(tech_response), tech_status

    return jsonify({
        "message": "Técnico registrado correctamente",
        "token": user_response["token"],
        "user": user_response["user"],
        "technician": tech_response
    }), 201

#Creamos la ruta que tendra la funcion de inicio de sesión
@auth_bp.route("/login",methods=["POST"])
def login():
    #Creamos variable que contiene el metodo y codigo de estado
    data,status = UserRegister.login(request.json)

    #Retoramos mensaje de resultado con el codigo de estado
    return jsonify(data),status