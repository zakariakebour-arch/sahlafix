from pydantic import BaseModel, EmailStr, field_validator
import re

class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    role: str | None = "user" #Rol es un string y si no se selecciona que rol es, se asigna user por defecto

    # Validador de contraseña
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if len(value) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres.")

        #Aqui creamos reglas para la varificacion correcta de contraseña
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        if not re.search(r"[^\w\s]", value):
            raise ValueError("La contraseña debe contener al menos un símbolo especial.")

        return value

