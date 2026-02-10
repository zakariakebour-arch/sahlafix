from app.extensions import db

#Creamos la clase categoria que define la tabla categorias
class Category(db.Model):
    #Nombre de la tabla en Mysql
    __tablename__ = "categories"

    #Columna identificador clave primaria
    id = db.Column(db.Integer, primary_key=True)

    #Columna nombre no nula
    name = db.Column(db.String(100), nullable=False)

    #Slug no nulo y unico
    slug = db.Column(db.String(100), nullable=False, unique=True)

    