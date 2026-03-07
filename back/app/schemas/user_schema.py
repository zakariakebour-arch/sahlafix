from pydantic import BaseModel, EmailStr, field_validator
import re

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: str | None = "user"  # Rol es un string y si no se selecciona que rol es, se asigna user por defecto

    full_name: str
    # Validador de contraseña
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:  # corregido <
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        # Aqui creamos reglas para la verificación correcta de contraseña
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[^\w\s]", value):
            raise ValueError("La contraseña debe contener al menos un símbolo especial.")

        return value

    # Validador opcional del rol (recomendado)
    @field_validator("role")
    @classmethod
    def validate_role(cls, value: str):
        # Si no se pasa nada, el valor por defecto "user" es válido
        valid_roles = ["user", "technician", "admin"]
        if value not in valid_roles:
            raise ValueError(f"El rol debe ser uno de: {valid_roles}")
        return value


# Clase para validar el login, solo necesita email y contraseña para ello
class UserLoginSchema(BaseModel):
    # Correo
    email: EmailStr
    
    # Contraseña
    password: str

#Creamos clase que valide los datos de ubicacion
class UserLocationSchema(BaseModel):

    latitude: float
    longitude: float

    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value):
        if value < -90 or value > 90:
            raise ValueError("Latitud inválida")
        return value

    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value):
        if value < -180 or value > 180:
            raise ValueError("Longitud inválida")
        return value