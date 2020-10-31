from app.main import create_app
from fastapi.testclient import TestClient
import pytest
from app.database import Database
from app.routers.employees import get_db

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


test_employee = {"first_name": "Test name",
                 "last_name": "lastname",
                 "gender": "M",
                 "date_of_birth": "2000-01-01",
                 "address": "Test address",
                 "phone": "000-000-000",
                 "email": "test@demo.pl",
                 "id_number": "11111111111",
                 "salary": 30000}


def test_add_employee(client):
    response = client.post("/fast_delivery/employee/add", json=test_employee)
    assert response.status_code == 200
    assert response.json() == {"first_name": "Test name",
                               "last_name": "lastname",
                               "gender": "M",
                               "date_of_birth": "2000-01-01",
                               "address": "Test address",
                               "phone": "000-000-000",
                               "email": "test@demo.pl",
                               "id_number": "11111111111",
                               "salary": 30000}
