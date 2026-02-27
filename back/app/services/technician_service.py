#Importamos la clase del modelo tecnicos
from app.models.technician import Technician
#Importamos schema para validar
from app.schemas.technician_schema import TechnicianCreateSchema
from pydantic import ValidationError
#Importamos base de datos
from app.extensions import db

class TechnicianService:
    #Creamos un metodo que selecciona segun el id y es un metodo estatico
    @staticmethod
    def get_by_id(technician_id: int):
        #Un filtro que compara el parametro(id) que recebiremos en el endpoint 
        technicians = Technician.query.filter_by(id=technician_id).first()

        #Si no exsiste el tecnico
        if not technicians:
            return {"error":"Tecnico no encontrado"},404
        
        #Retornamos la informacion del tecnico
        return technicians.to_dict(),200
    
    #Metodo para devolver todos los tecnicos disponibles en el sistema
    @staticmethod
    def get_technicians():
        #Todos los tecnicos disponibles en la base de datos
        technicians = Technician.query.all()

        #Retornamos lo tecnicos  
        return [t.to_dict() for t in technicians],200
    
    #Metodo para crear tecnico
    @staticmethod
    def create_technician(data: dict):  # Le entra como parametro un diccionario
        try:
            #validamos los datos
            validate_data = TechnicianCreateSchema(**data)
        except ValidationError as e:
            return {"error": e.errors()}, 400

        try:
            #Creamos el nuevo tecnico
            new_technician = Technician(
                full_name=validate_data.full_name,
                wilaya=validate_data.wilaya,
                city=validate_data.city,
                description=validate_data.description,
                phone=validate_data.phone,        
                category_id=validate_data.category_id,
                user_id=validate_data.user_id,    
                is_active=validate_data.is_active 
            )

            #Lo guardamos en la base de datos
            db.session.add(new_technician)
            db.session.commit()

            #Retornamos el tecnico creado
            return new_technician.to_dict(), 201

        except Exception:
            db.session.rollback()
            #Mensaje del error
            return {"error": "Error interno"}, 500