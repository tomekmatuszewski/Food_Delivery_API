from app.main import create_app
from fastapi.testclient import TestClient
import pytest
from app.routers.clients import get_db
from app.database import Database

test_db = Database('sqlite://')
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


data = {"company_name": "Test name",
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "000000000",
        "company_id": "0000"}


def test_add_client(client):
    response = client.post("/fast_delivery/client/add", json=data)
    assert response.status_code == 200
    assert response.json() == {"company_name": "Test name",
                               "address": "test_address",
                               "contact_person": "Test Person",
                               "phone": "000-000-000",
                               "email": "test@demo.pl",
                               "tax_identification_number": "000000000",
                               "company_id": "0000"}
