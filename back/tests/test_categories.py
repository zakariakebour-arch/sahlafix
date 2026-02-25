# tests/test_categories.py
import pytest
from app import create_app
from app.extensions import db
from app.models.category import Category
from flask import url_for
import json

# -----------------------------
# Fixtures
# -----------------------------

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
def init_categories(app):
    """Crea categorías de prueba en la DB"""
    categories = [
        Category(name="Electricidad", slug="electricidad"),
        Category(name="Plomería", slug="plomeria"),
        Category(name="Carpintería", slug="carpinteria"),
    ]
    db.session.add_all(categories)
    db.session.commit()
    return categories

# -----------------------------
# Tests
# -----------------------------

def test_get_all_categories(client, init_categories):
    """Probar endpoint GET /categories"""
    response = client.get("/api/v1/categories/")
    assert response.status_code == 200

    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert any(c["name"] == "Electricidad" for c in data)

def test_get_category_by_id(client, init_categories):
    """Probar endpoint GET /categories/<id>"""
    category_id = init_categories[0].id
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["name"] == "Electricidad"

def test_get_category_not_found(client):
    """Probar endpoint GET /categories/<id> inexistente"""
    response = client.get("/api/v1/categories/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data