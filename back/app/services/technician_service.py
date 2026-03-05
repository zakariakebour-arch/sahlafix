#Importamos la clase del modelo tecnicos
from app.models.technician import Technician
#Importamos schema para validar
from app.schemas.technician_schema import TechnicianCreateSchema
from app.models.user import User
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
            return {"error": str(e)}, 400

        # Normalizar teléfono
        phone = validate_data.phone
        if not phone.startswith("+"):
            phone = "+34" + phone

        # Verificar si ya existe un técnico con ese nombre y teléfono 
        existing_technician = Technician.query.filter_by(full_name=validate_data.full_name, phone=validate_data.phone ).first()

        #Si exsiste con esos datos
        if existing_technician:
            return {"error":"Hay tecnico registrado con esos datos en el sistema"},409
        
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
                is_active=validate_data.is_active,
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
        
    #Metodo para busqueda
    @staticmethod
    def search_by_name(name:str):
        # Buscamos usuarios y técnicos, usando Technician.full_name
        results = db.session.query(User, Technician)\
            .outerjoin(Technician, Technician.user_id == User.id)\
            .filter(Technician.full_name.ilike(f"%{name}%"))\
            .all()
        
        # Expunigir el objeto para que no quede en sesion
        for user, tech in results:
            db.session.expunge(user)
            if tech:
                db.session.expunge(tech)
            # Formateamos resultado

        data = []
        for user, technician in results:
            item = {
                "user_id": user.id,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            }
            if technician:
                # Añadimos datos de técnico si existen
                item.update({
                    "technician_id": technician.id,
                    "full_name": technician.full_name,
                    "category_id": technician.category_id,
                    "city": technician.city,
                    "wilaya": technician.wilaya,
                    "description": technician.description,
                    "image_url": technician.photo_profile,
                })
            data.append(item)
            #Si no encuentra nada
        return data, 200
        
