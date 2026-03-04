#Importamos para hashear contraseñas
from werkzeug.security import generate_password_hash, check_password_hash
#Importamos db desde extensions
from app.extensions import db
from pydantic import ValidationError
from app.models.user import User
#Importamos validador
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema
#Importamos JWT
from app.utils.security import generate_token
from typing import Optional

class UserRegister:

  @staticmethod #Metodo estatico
  def create_user(data: dict):  #Le entra parametro como diccionario
    #Hacemos un try para validar con pydantic
    try:
      validate_data = UserCreateSchema(**data)
    except ValidationError as e:
      print(e.errors())
      return {
        "error": "Datos inválidos",
        "details": str(e)  #Detalle del error
      }, 400

    # Normalizamos antes el correo
    email = validate_data.email.strip().lower()

    #Variable que comprueba si ya exsiste el usuario
    existing_user = User.query.filter_by(email=email).first()

    #Si ya exsiste el usuario entonces reotrnamos un mensaje
    if existing_user:
      return {"error": "Usuario ya registrado"}, 409

    #Cremos la contraseña hasheada
    password_hash = generate_password_hash(validate_data.password)

    #Creamos nuevo usuario
    new_user = User(
      email=email,
      password_hash=password_hash,   #Corrección: nombre correcto de columna
      role=validate_data.role
    )

    #Hacemos un try para conexion con la base de datos por si falla
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error al crear usuario:", e)
        return {"error": "Error interno del servidor"}, 500

    #Generamos token
    token = generate_token(new_user)

    #Retornamos un mensaje de exsito
    return {
      "message": "Usuario creado correctamente",
      "token": token,
      "user": {
        "id": new_user.id,
        "email": new_user.email,
        "role": new_user.role
      }
    }, 201


  @staticmethod #Metodo estatico
  def login(data: dict): #Le entra parametro como diccionario
    #Validamos data antes de comprobar si exsiste el usuario
    try:
      validate_data = UserLoginSchema(**data)
    except ValidationError as e:
      return {
        "error": "datos inválidos",
        "details": str(e)
      }, 400
    
    #Normalizamos antes el correo
    email = validate_data.email.strip().lower()

    #Hacemos consulta de todos los correos de usuarios o clientes disponibles
    user = User.query.filter_by(email=email).first()

    #Comprobamos correo del usuario y contraseña
    if not user or not check_password_hash(user.password_hash, validate_data.password):
      return {
        "error": "Credenciales incorrectas"
      }, 401
    
    #Variable que genera el token para el usuario
    token = generate_token(user)
    
    #Mensaje de exsito 
    return {
      "message": "exito",
      "token": token,
      "user": {
        "id": user.id,
        "email": user.email,
        "role": user.role
      }
    }, 200