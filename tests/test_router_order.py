import os
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import Database
from app.main import create_app
from app.models import Client, Order
from app.routers.orders import get_db

BASE_DIR = Path(__file__).parent
app = create_app()


@pytest.fixture(name="db", scope="module")
def create_db() -> Session:
    test_db = Database(f"sqlite:///{BASE_DIR}/test.db")
    db = test_db.SessionLocal()
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
        "full_price": 150,
    },
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": 55,
        "destination_address": "Kraków, Wielopole 1",
        "full_price": 150,
    },
]


def test_get_orders(client):
    response = client.get("/fast_delivery/orders")
    assert response.status_code == 200


test_client = {
    "company_name": "Test name",
    "address": "test_address",
    "contact_person": "Test Person",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "tax_identification_number": "000000000",
    "company_id": "0000",
}


@patch("app.routers.utils.requests.get")
def test_add_order(mock_get, client, db):
    cli1 = Client(**test_client)
    db.add(cli1)
    db.commit()
    mock_get.json.return_value = {"distance": 1.0}
    response = client.post("/fast_delivery/orders", json=test_order[0])
    assert response.status_code == 200
    assert db.query(Order.distance).filter(Order.id == 1).first()[0] == 1.61
    response = client.post("/fast_delivery/orders", json=test_order[1])
    assert response.status_code == 422


order_updated_dict = {
    "employee_id": 1,
    "client_id": 1,
    "contact_phone": "555-666-999",
    "destination_address": "Kraków, Wielopole 10",
    "full_price": 200.00,
}


@patch("app.routers.utils.requests.get")
def test_update_order(mock_get, client, db):
    mock_get.json.return_value = {"distance": 1.0}

    response = client.put("/fast_delivery/orders/1/update", json=order_updated_dict)
    assert response.status_code == 200
    assert response.json() == {
        "client_id": 1,
        "contact_phone": "555-666-999",
        "date": date.today().strftime("%Y-%m-%d"),
        "destination_address": "Kraków, Wielopole 10",
        "distance": 1.61,
        "employee_id": 1,
        "full_price": 200.0,
        "id": 1,
        "other_info": None,
    }


def test_delete_order(client, db):
    response = client.delete("fast_delivery/orders/1/delete")
    assert response.status_code == 200
    assert db.query(Order).count() == 0
