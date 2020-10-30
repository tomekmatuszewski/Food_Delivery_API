from app.main import create_app
from fastapi.testclient import TestClient
import pytest
from app import database
from app.routers.clients import get_db

app = create_app()
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


def test_add_client(client):
    data = {"company_name": "Test name",
            "address": "test_address"}
    response = client.post("/fast_delivery/client/add", json=data)
    assert response.status_code == 200
    assert response.json() == {"company_name": "Test name",
                               "address": "test_address"}
