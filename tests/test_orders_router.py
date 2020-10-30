from sqlalchemy.orm import Session
import os
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import database
from app.main import create_app
from app.models import Client, Order
from app.routers.orders import get_db
from app.routers.utils import get_distance

app = create_app()
BASE_DIR = Path(__file__).parent

@pytest.fixture(name="db")
def create_db() -> Session:
    database.init_db(f"sqlite:///{BASE_DIR}/test.db")
    db = database.SessionLocal()
    yield db
    os.remove(f"{BASE_DIR}/test.db")


@pytest.fixture(name="client")
def client(db) -> TestClient:
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client

test_order = [
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": "000-000-000",
        "destination_address": "Kraków, Wielopole 1",
        "full_price": 150
    },
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": 55,
        "destination_address": "Kraków, Wielopole 1",
        "full_price": 150
    }
]


def test_get_orders(client):
    response = client.get("/fast_delivery/orders")
    assert response.status_code == 200


@patch('app.routers.utils.requests.get')
def test_get_distance(mock_get):
    mock_get.json.return_value = {"distance": 1.0}
    value = get_distance("Test address", "Test_address")
    assert value == 1.61


@patch('app.routers.utils.requests.get')
def test_add_order(mock_get, client, db):
    cli1 = Client(company_name="Test name", address="Kraków, Address")
    db.add(cli1)
    db.commit()
    mock_get.json.return_value = {"distance": 1.0}
    response = client.post("/fast_delivery/orders", json=test_order[0])
    assert response.status_code == 200
    assert db.query(Order.distance).filter(Order.id == 1).first()[0] == 1.61
    response = client.post("/fast_delivery/orders", json=test_order[1])
    assert response.status_code == 422