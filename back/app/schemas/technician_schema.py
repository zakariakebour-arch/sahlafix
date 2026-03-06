#Importamos pydantic
from pydantic import BaseModel, field_validator

#Importamos opcion para datos opcionales
from typing import Optional

#Importamos validador profesional de numeros de telefono
import phonenumbers


#Creamos la clase TechnicianCreateSchema que sera la encargada de validar la creacion del tecnico
class TechnicianCreateSchema(BaseModel):

    #Nombre completo como string
    full_name: str

    #Identificador de categoria como numeroAC
    category_id: int

    #Wilaya como string
    wilaya: str

    #Ciudad opcional string si no se selecciona no se asigna ningun valor
    city: Optional[str] = None

    #Descripcion opcional y si no se asigna valor vacio
    description: Optional[str] = None

    #Activo tipo boleano y por defecto es True(osea activo)
    is_active: bool = True

    #Numero telefono (luego sera convertido a formato E164)
    phone: str

    #Usuario id como numero entero
    user_id: int

    #Latitud opcional
    latitude: Optional[float] = None

    #Longitud opcional
    longitude: Optional[float] = None


    #Validador de nombre
    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        if len(value.strip()) < 3:
            raise ValueError("El nombre completo debe tener al menos 3 caracteres.")
        return value


    #Validador de categoria id
    @field_validator("category_id")
    @classmethod
    def validate_category_id(cls, value: int):
        if value <= 0:
            raise ValueError("category_id debe ser un entero válido.")
        return value


    #Validador de valor wilaya
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
        if value and len(value.strip()) < 2:
            raise ValueError("La ciudad no es válida.")
        return value


    #Validador de descripcion
    @field_validator("description")
    @classmethod
    def validate_description(cls, value: Optional[str]):
        if value and len(value) > 500:
            raise ValueError("La descripción no puede superar los 500 caracteres.")
        return value


    #Validador de latitud
    @field_validator("latitude")
    @classmethod
    def validate_latitude(cls, value: Optional[float]):
        if value is None:
            return value

        if value < -90 or value > 90:
            raise ValueError("La latitud debe estar entre -90 y 90.")

        return value


    #Validador de longitud
    @field_validator("longitude")
    @classmethod
    def validate_longitude(cls, value: Optional[float]):
        if value is None:
            return value

        if value < -180 or value > 180:
            raise ValueError("La longitud debe estar entre -180 y 180.")

        return value


    #Validamos por completo y de manera profesional con la libreria phonenumbers
    @field_validator("phone")
    @classmethod
    def validate_and_normalize_phone(cls, v: str) -> str:

        raw = (v or "").strip()

        if not raw:
            raise ValueError("El teléfono es obligatorio")

        # Asignamos de momento origenes españa y argelia
        candidate_regions = ["DZ", "ES"]

        # Si ya viene con '+', probar internacional directo
        if raw.startswith("+"):
            try:
                num = phonenumbers.parse(raw, None)
                if phonenumbers.is_valid_number(num):
                    return phonenumbers.format_number(
                        num, phonenumbers.PhoneNumberFormat.E164
                    )
            except Exception:
                pass

        # Probar por regiones conocidas
        for region in candidate_regions:
            try:
                num = phonenumbers.parse(raw, region)
                if phonenumbers.is_valid_number(num):
                    return phonenumbers.format_number(
                        num, phonenumbers.PhoneNumberFormat.E164
                    )
            except Exception:
                continue

        # Mensaje final si no es válido
        raise ValueError(
            "Número de teléfono inválido. Usa formato internacional (+34..., +213...) o un número local válido."
        )

