#Importamos schema de categorias
from app.schemas.category_schema import CategoryCreateSchema
#Importamos el modelo
from app.models.category import Category
#Importamos la base de datos
from app.extensions import db
#Importamos validador de error de pydantic
from pydantic import ValidationError

#Creamos la clase de sevicio de categorias
class CategoriesService:
    #Metodo estatico para recibir la categoria del tecnico segun el id
    @staticmethod
    def get_category(category_id: int):
        #Hacemos consulta que busca la categoria del tecnico segun el identificador
        Category.query.filter_by(id=category_id).first()

    #Metodo estatico para que devuelva todas las categorias en una lista
    @staticmethod
    def get_categories():
        categories = Category.query.all()
        #Filtramos
        return [c.to_dict() for c in categories]
    
    #Metodo estatico para crear nueva categoria
    @staticmethod
    def create(data: dict):
        try:
            #Como primero validamos el diccionario con schema de categorias
            validate_data = CategoryCreateSchema(**data)

        except ValidationError as e:
           return {"error":"Datos incorrectos",
                "details":e.errors()
                },400
    
    #Metodo estatico para actualizar categoria
    @staticmethod
    def update(category_id: int, data: dict):#Nos entra la nueva actualizacion y el identificador de la categoria como parametro
        pass

    #Metodo estatico para eliminar categorias
    @staticmethod
    def delete(category_id: int):
        pass
    