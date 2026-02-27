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
        category = Category.query.filter_by(id=category_id).first()

        #Si no exsiste la categoria
        if not category:
            return {"error":"Categoria no encontrada"},404
        
        #Retornamos la categoria 
        return category.to_dict(),200
    
    #Metodo estatico para que devuelva todas las categorias en una lista
    @staticmethod
    def get_categories():
        categories = Category.query.all()
        #Filtramos
        return [c.to_dict() for c in categories],200
    
    #Metodo estatico para crear nueva categoria
    @staticmethod
    def create(data: dict):
        try:
            #Como primero validamos el diccionario con schema de categorias
            validate_data = CategoryCreateSchema(**data)

            #Creamos la nueva categoria para insertar en la base de datos
            new_category = Category(
                name=validate_data.name,
                slug=validate_data.slug,
            )

            #Intentamos insertar si falla lanzamos un mensaje de error
            try:
                db.session.add(new_category)
                db.session.commit()
            except ValueError:
                db.session.rollback()
                return {
                    "error":"Error interno"
                },500
        except ValidationError as e:
           return {"error":"Datos incorrectos",
                "details":e.errors()
                },400

        #Retor que se creo de manera correcta 
        return new_category.to_dict(),201
    
    #Metodo estatico para actualizar categoria
    @staticmethod
    def update(category_id: int, data: dict): #Nos entra la nueva actualizacion y el identificador de la categoria como parametro
        #Como primer paso validamos los datos que nos llegan con schema
        try:
            validate_data = CategoryCreateSchema(**data)
        except ValidationError as e:
            return {"error":"Datos inválidos", "details": e.errors()}, 400
        
        #Buscamos si exsiste la categoria
        category = Category.query.filter_by(id=category_id).first()

        #Si no exsiste
        if not category:
            return {"error":"categoria no encontrada"},404
        
        #Hacemos un try porque si falla la ejecucion falla el sistema
        try:
            #Datos a actualizar
            category.name = validate_data.name
            category.slug = validate_data.slug
            category.is_active = validate_data.is_active  # Añadido
            
            #Guardamos cambio
            db.session.commit()

            #Retornamos la categoria
            return category.to_dict(), 200
        
        except Exception:
            db.session.rollback()
            return {"error":"Error interno"},500

    #Metodo estatico para eliminar categorias
    @staticmethod
    def delete(category_id: int):
        #Buscamos la categoria
        category = Category.query.get(category_id)
            
        #Si no se encuentra la categoria que deseamos eliminar
        if not category:
            return {
                "error":"Categoria no encontrada"
            },404

        try:
            #Eliminamos la categoria disponible
            db.session.delete(category)
            db.session.commit()
        except Exception:
            #mensaje si falla
            return {"error":"Error interno"},500

        return {"message":"categoria eliminada correctamente"},200