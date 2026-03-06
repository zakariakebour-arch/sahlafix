from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    # Clave primaria
    id = db.Column(db.Integer, primary_key=True)

    # Correo único
    email = db.Column(db.String(255), unique=True, nullable=False)

    # Contraseña hasheada
    password_hash = db.Column(db.String(255), nullable=False)

    # Rol del usuario 
    role = db.Column(db.String(50), nullable=False)

    # Teléfono opcional (solo usado si el usuario no es técnico, ya que el técnico tiene su propio teléfono)
    phone = db.Column(db.String(20), nullable=True)

    # Fecha de creación
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relación 1 a 1 con Technician
    technician = db.relationship("Technician", backref="user", uselist=False)

    #Latitud del usuario
    latitude = db.Column(db.Float, nullable=True)

    #Longitud del usuario
    longitude = db.Column(db.Float, nullable=True)