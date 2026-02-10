from pydantic import BaseModel, field_validator
from typing import Optional

class TechnicianCreateSchema(BaseModel):
    #Nombre completo como string
    full_name: str

    #Identificador de categoria como numero
    category_id: int

    #Wilaya como string
    wilaya: str

    #Ciudad opcional string si no se selecciona no se asigna ningun valor
    city: Optional[str] = None

    #Descripcion opcional y si no se asigna valor vacio
    description: Optional[str] = None

    #Activo tipo boleano y por defecto es True(osea activo)
    is_active: bool = True

    #Validador de nombre
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):#Entra parametro  
        if len(value.strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres.")
        return value

    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int):
        if value <= 0:
            raise ValueError("category_id debe ser un entero válido.")
        return value

    @field_validator("wilaya")
    @classmethod
    def validate_wilaya(cls, value: str):
        if len(value.strip()) < 2:
            raise ValueError("La wilaya no es válida.")
        return value

    #Validador de ciudad
    @field_validator("city")
    @classmethod
    def validate_city(cls, value: Optional[str]):
        if value and len(value.strip()) < 2:#Si valor se ha seleccioando y es menor que 2 caracteres sin espacio da error
            raise ValueError("La ciudad no es válida.")
        return value #De lo contrario retorna el valor como es correcto

    #Validador de descripcion
    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]):#Le entra el parametro opcional
        if value and len(value) > 500:#Si se ha seleccionado el parametro y es mayor que 500 caracteres,lanzamos el error
            raise ValueError("La descripción no puede superar los 500 caracteres.")
        return value

