import pytest
from app import create_app
from app.extensions import db

@pytest.fixture
def app():
    """Crear app en modo testing con BD en memoria"""
    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_user(client):
    response = client.post("/api/v1/auth/register", json={
        "email": "testuser@example.com",
        "password": "password123",
        "role": "technician"
    })

    data = response.get_json()
    assert response.status_code == 201
    assert data["email"] == "testuser@example.com"


def test_login_user_success(client):
    client.post("/api/v1/auth/register", json={
        "email": "testlogin@example.com",
        "password": "password123",
        "role": "technician"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "testlogin@example.com",
        "password": "password123"
    })

    data = response.get_json()
    assert response.status_code == 200
    assert "access_token" in data


def test_login_user_failure(client):
    client.post("/api/v1/auth/register", json={
        "email": "wrongpass@example.com",
        "password": "password123",
        "role": "user"
    })

    response = client.post("/api/v1/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "incorrect"
    })

    assert response.status_code == 401


def test_protected_endpoint_requires_auth(client):
    response = client.get("/api/v1/technicians/")
    assert response.status_code == 401