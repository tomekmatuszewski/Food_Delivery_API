import pytest
from fastapi.testclient import TestClient

from app.database import Database
from app.main import create_app
from app.routers.employees import get_db

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


test_employee = {
    "first_name": "Test name",
    "last_name": "lastname",
    "gender": "M",
    "date_of_birth": "2000-01-01",
    "address": "Test address",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "id_number": "11111111111",
    "salary": 30000,
}


def test_add_employee(client):
    response = client.post("/fast_delivery/employees", json=test_employee)
    assert response.status_code == 200
    assert response.json() == {'address': 'Test address',
                               'date_of_birth': '2000-01-01',
                               'email': 'test@demo.pl',
                               'first_name': 'Test name',
                               'gender': 'M',
                               'id': 1,
                               'id_number': '11111111111',
                               'last_name': 'lastname',
                               'phone': '000-000-000',
                               'salary': 30000.0}
