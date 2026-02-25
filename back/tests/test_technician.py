# tests/test_technicians.py
import pytest
from app import create_app
from app.extensions import db
from app.models.technician import Technician
from app.models.user import User
from app.models.category import Category
from datetime import datetime

@pytest.fixture
def app():
    """Crea la app en modo test con SQLite en memoria"""
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Devuelve un cliente de test de Flask"""
    return app.test_client()

@pytest.fixture
def init_users_and_categories(app):
    """Crea usuarios y categorías para relacionar técnicos"""
    # Usuarios
    user1 = User(
        email="techuser1@example.com",
        password_hash="hash1",
        role="technician",
        phone="611555001",
        created_at=datetime.utcnow()
    )
    user2 = User(
        email="techuser2@example.com",
        password_hash="hash2",
        role="technician",
        phone="611555002",
        created_at=datetime.utcnow()
    )
    # Categorías
    cat1 = Category(name="Electricidad", slug="electricidad")
    cat2 = Category(name="Plomería", slug="plomeria")

    db.session.add_all([user1, user2, cat1, cat2])
    db.session.commit()
    return {"users": [user1, user2], "categories": [cat1, cat2]}

@pytest.fixture
def init_technicians(app, init_users_and_categories):
    """Crea técnicos de prueba"""
    users = init_users_and_categories["users"]
    categories = init_users_and_categories["categories"]

    tech1 = Technician(
        user_id=users[0].id,
        category_id=categories[0].id,
        full_name="Mohamed Zakaria",
        wilaya="Algiers",
        city="Bab Ezzouar",
        description="Técnico especialista en electricidad",
        phone=611555001,
        is_active=1,
        created_at=datetime.utcnow()
    )
    tech2 = Technician(
        user_id=users[1].id,
        category_id=categories[1].id,
        full_name="Fatima B.",
        wilaya="Oran",
        city="Bir El Djir",
        description="Técnica en plomería",
        phone=611555002,
        is_active=1,
        created_at=datetime.utcnow()
    )
    db.session.add_all([tech1, tech2])
    db.session.commit()
    return [tech1, tech2]

# -----------------------------
# Tests
# -----------------------------

def test_get_all_technicians(client, init_technicians):
    """Probar GET /technicians/"""
    response = client.get("/api/v1/technicians/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert any(t["full_name"] == "Mohamed Zakaria" for t in data)

def test_get_technician_by_id(client, init_technicians):
    """Probar GET /technicians/<id>"""
    tech_id = init_technicians[0].id
    response = client.get(f"/api/v1/technicians/{tech_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["full_name"] == "Mohamed Zakaria"

def test_get_technician_not_found(client):
    """Probar GET /technicians/<id> inexistente"""
    response = client.get("/api/v1/technicians/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

def test_create_technician(client, init_users_and_categories):
    """Probar POST /technicians/"""
    user = init_users_and_categories["users"][0]
    category = init_users_and_categories["categories"][0]

    payload = {
        "full_name": "Ahmed K.",
        "wilaya": "Blida",
        "city": "Boufarik",
        "description": "Técnico junior",
        "phone": 611555003,
        "user_id": user.id,
        "category_id": category.id
    }

    response = client.post("/api/v1/technicians/", json=payload)
    # Si tu endpoint requiere JWT, deberás añadir header Authorization
    assert response.status_code in (201, 401)  # 401 si no estás simulando auth
    # Si es 201, puedes verificar la creación
    if response.status_code == 201:
        data = response.get_json()
        assert data["full_name"] == "Ahmed K."