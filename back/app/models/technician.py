from app.extensions import db
from datetime import datetime
from app.models.category import Category
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

    #Relacion con categoria
    category = db.relationship("Category", back_populates="technicians")

    #Nombre completo
    full_name = db.Column(db.String(255), nullable=False)

    #Columna wilaya
    wilaya = db.Column(db.String(100), nullable=False)

    #Columna ciudad
    city = db.Column(db.String(100), nullable=True)

    #Descripcion del tecnico
    description = db.Column(db.String(255), nullable=True)

    #Columna telefono (CORREGIDO: antes Integer → ahora String)
    phone = db.Column(db.String(20), nullable=False)

    #Columna que solo guarda la foto
    photo_profile = db.Column(db.String(255), nullable=True)

    #Activo o no activo el tecnico
    is_active = db.Column(db.Boolean, default=True)

    #Columna que registra el tiempo de creacion
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    #Columnas de longitud y latitud para calcular y posicionar tecnicos en el mapa
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    #Para guardar la ubicacion reciente
    last_location_update = db.Column(db.DateTime, nullable=True)

    
    available = db.Column(db.Boolean, default=True, nullable=False)

    #Creamos un metodo que retorna un diccionario con la información asociada al tecnico
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.full_name,
            "description": self.description,
            "category_id": self.category_id,
            "image_url": self.photo_profile,
            "category_name":self.category.name,
            "wilaya":self.wilaya,
            "city":self.city,
            "latitude":self.latitude,
            "longitude":self.longitude,
            "last_location":self.last_location_update
        }