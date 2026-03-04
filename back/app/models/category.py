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

    #Relacion con la tabla tecnicos
    technicians = db.relationship("Technician", back_populates="category")

    #Creamos un metodo que devuelve un diccionario listo para que sea un JSON valido 
    def to_dict(self, include_technicians=False):
        #Objeto que contiene el resultado de las columnas del modelo 
        data = {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
        }

        #Para poder filtar tecnicos segun categoria,tenemos que tener en cuenta la relacion y para filtrarla comprbamos si ya esta disponible para no entrar en recursion entre categoria y tecnicos
        if include_technicians:
            data["technicians"] = [t.id for t in self.technicians] #Solo devuelve y filtra id de tecnicos

        return data