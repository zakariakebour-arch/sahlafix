from app.extensions import db

#Creamos la clase que define la tabla
class Technician(db.Model):

    #Nombre de la tabla
    __tablename__ = "technicians"

    #Identificador de la tabla
    id = db.Column(db.Integer, primary_key=True)

    #Clave foranea para relacion con la tabla usuario
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    #Columna categoria
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False
    )

    #Nombre completo
    full_name = db.Column(db.String(255), nullable=False)

    #Columna wilaya
    wilaya = db.Column(db.String(100), nullable=False)

    #Columna ciudad
    city = db.Column(db.String(100), nullable=True)

    #Descripcion del tecnico
    description = db.Column(db.String(255),nullable=True)

    #Columna telefono
    phone = db.Column(db.Integer,nullable=False)

    #Columna que solo guarda la foto
    photo_profile = db.Column(db.String(255),nullable=True)

    #Activo o no activo el tenico
    is_active = db.Column(db.Boolean, default=True)

    #Columna que registra el tiempo de creacion
    created_at = db.Column(db.DateTime, nullable=False)

    #Creamos un metodo que retorna un diccionario con la información asiciada al tecnico
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.full_name,
            "description":self.description,
            "category_id":self.category_id,
            "image_url":self.photo_profile
        } 

