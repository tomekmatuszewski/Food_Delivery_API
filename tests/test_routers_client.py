import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.routers.clients import get_db

test_db = Database("sqlite://")
app = create_app()


def override_get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(name="client")
def client():
    with TestClient(app) as client:
        yield client


data = {
    "company_name": "Test name",
    "address": "test_address",
    "contact_person": "Test Person",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "tax_identification_number": "000000000",
    "company_id": "0000",
}


def test_add_client(client):
    response = client.post("/fast_delivery/clients", json=data)
    assert response.status_code == 200
    assert response.json() == {'address': 'test_address',
                               'company_id': '0000',
                               'company_name': 'Test name',
                               'contact_person': 'Test Person',
                               'email': 'test@demo.pl',
                               'id': 1,
                               'phone': '000-000-000',
                               'tax_identification_number': '000000000'}
