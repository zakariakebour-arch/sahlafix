from pydantic import BaseModel, field_validator
import re

#Creamos la clase que validara los datos
class CategoryCreateSchema(BaseModel):
    name: str
    slug: str
    is_active: bool = True

    #Validamos de manera mas estricta
    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str):#Entra un parametro como string
        if len(value.strip()) < 2:#Esta condicion comprueba si el nombre es menor que 2 y sin espacio
            raise ValueError("El nombre de la categoría es demasiado corto.")
        return value

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, value: str):
        if not re.match(r"^[a-z0-9-]+$", value):#Comprobamos que solo tenga valores entre a-z(letras minusculas) y numeros,
            raise ValueError(
                "El slug solo puede contener letras minúsculas, números y guiones."
            )
        return value

