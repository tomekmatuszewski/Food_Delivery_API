from app.main import app
from fastapi.testclient import TestClient
import pytest
from app import database
from app.routers.employees import get_db
from app.models import Employee


database.init_db('sqlite://')


def override_get_db():
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(name="client")
def client():
    with TestClient(app) as client:
        yield client


def test_add_employee(client):
    data = {"first_name": "Test name",
            "last_name": "Test lastname"}
    response = client.post("/fast_delivery/employee/add", json=data)
    assert response.status_code == 200
    assert response.json() == {"first_name": "Test name",
                               "last_name": "Test lastname"}