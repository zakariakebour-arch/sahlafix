#Importamos la clase del modelo tecnicos 
from app.models.technician import Technician

class TechnicianService:
    #Creamos un metodo que selecciona segun el id y es un metodo estatico
    @staticmethod
    def get_by_id(technician_id: int):
        #Retornamos un filtro que compara el parametro(id) que recebiremos en el endpoint 
        return Technician.query.filter_by(id=technician_id).first()
    


