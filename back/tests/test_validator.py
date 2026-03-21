import pytest
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema
from pydantic import ValidationError

# --- UserCreateSchema ---

# Camino 1: registro correcto
def test_registro_valido():
    data = UserCreateSchema(
        email="test@test.com",
        password="Abcdef1!",
        role="user",
        full_name="Test User"
    )
    assert data.email == "test@test.com"

# Camino 2: contraseña muy corta
def test_password_muy_corta():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="Ab1!", role="user", full_name="Test User")

# Camino 3: contraseña sin mayúscula
def test_password_sin_mayuscula():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="abcdef1!", role="user", full_name="Test User")

# Camino 4: contraseña sin minúscula
def test_password_sin_minuscula():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="ABCDEF1!", role="user", full_name="Test User")

# Camino 5: contraseña sin número
def test_password_sin_numero():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="Abcdefg!", role="user", full_name="Test User")

# Camino 6: contraseña sin símbolo especial
def test_password_sin_simbolo():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="Abcdef12", role="user", full_name="Test User")

# Camino 7: email inválido
def test_email_invalido():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="noesuncorreo", password="Abcdef1!", role="user", full_name="Test User")

# Camino 8: rol inválido
def test_rol_invalido():
    with pytest.raises(ValidationError):
        UserCreateSchema(email="test@test.com", password="Abcdef1!", role="superadmin", full_name="Test User")

# Camino 9: rol válido technician
def test_rol_technician():
    data = UserCreateSchema(
        email="tech@test.com",
        password="Abcdef1!",
        role="technician",
        full_name="Tech User"
    )
    assert data.role == "technician"

# --- UserLoginSchema ---

# Camino 10: login schema válido
def test_login_schema_valido():
    data = UserLoginSchema(email="test@test.com", password="cualquiera")
    assert data.email == "test@test.com"

# Camino 11: login sin email
def test_login_sin_email():
    with pytest.raises(ValidationError):
        UserLoginSchema(password="Abcdef1!")

# Camino 12: login sin password
def test_login_sin_password():
    with pytest.raises(ValidationError):
        UserLoginSchema(email="test@test.com")