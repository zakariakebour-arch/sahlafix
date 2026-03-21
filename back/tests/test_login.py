import pytest
from unittest.mock import patch, MagicMock
from app.services.user_service import UserRegister

# Camino 1: falta el email
def test_login_schema_sin_email():
    data = {"password": "Abc1234!"}
    result, status = UserRegister.login(data)
    assert status == 400
    assert "error" in result

# Camino 2: email mal formado
def test_login_schema_email_invalido():
    data = {"email": "noesuncorreo", "password": "Abc1234!"}
    result, status = UserRegister.login(data)
    assert status == 400
    assert "error" in result

# Camino 3: falta la contraseña
def test_login_schema_sin_password():
    data = {"email": "test@test.com"}
    result, status = UserRegister.login(data)
    assert status == 400
    assert "error" in result

# Camino 4: usuario no existe en BD
@patch("app.services.user_service.User")
def test_login_usuario_no_existe(mock_user):
    mock_user.query.filter_by.return_value.first.return_value = None
    data = {"email": "noexiste@test.com", "password": "Abc1234!"}
    result, status = UserRegister.login(data)
    assert status == 401
    assert "error" in result

# Camino 5: contraseña incorrecta
@patch("app.services.user_service.check_password_hash")
@patch("app.services.user_service.User")
def test_login_password_incorrecta(mock_user, mock_check):
    mock_user.query.filter_by.return_value.first.return_value = MagicMock()
    mock_check.return_value = False
    data = {"email": "real@test.com", "password": "WrongPass1!"}
    result, status = UserRegister.login(data)
    assert status == 401
    assert "error" in result

# Camino 6: login correcto
@patch("app.services.user_service.generate_token")
@patch("app.services.user_service.check_password_hash")
@patch("app.services.user_service.User")
def test_login_correcto(mock_user, mock_check, mock_token):
    fake_user = MagicMock()
    fake_user.id = 1
    fake_user.email = "real@test.com"
    fake_user.full_name = "Test User"
    fake_user.role = "user"
    mock_user.query.filter_by.return_value.first.return_value = fake_user
    mock_check.return_value = True
    mock_token.return_value = "fake_token_123"
    data = {"email": "real@test.com", "password": "Correcto1!"}
    result, status = UserRegister.login(data)
    assert status == 200
    assert result["token"] == "fake_token_123"
    assert result["user"]["email"] == "real@test.com"