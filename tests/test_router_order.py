import os
from datetime import date
from pathlib import Path
from unittest.mock import patch
from datetime import date
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import Database
from app.main import app
from app.models import Client, Order, Employee
from app.routers.orders import get_db

BASE_DIR = Path(__file__).parent


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


test_client = {
    "company_name": "Test name",
    "address": "test_address",
    "contact_person": "Test Person",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "tax_identification_number": "000000000",
    "company_id": "0000",
}

test_employee = {
    "first_name": "Jack",
    "last_name": "Track",
    "gender": "M",
    "date_of_birth": "1991-01-01",
    "address": "Kraków, Kobierzyńska 1",
    "phone": "501-501-501",
    "email": "jdy@demo.pl",
    "id_number": "91010150033",
    "salary": 2000,
}

test_order = [
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": "500-600-000",
        "destination_address": "Kraków, Wielopole 1",
        "full_price": 100,
    },
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": 5,
        "destination_address": "Kraków, Wielopole 10",
        "full_price": 150,
    },
    {
        "employee_id": 1,
        "client_id": 1,
        "contact_phone": "600-600-700",
        "destination_address": "Kraków, Wielopole 10",
        "full_price": 200,
    },
]



@patch("app.routers.utils.requests.get")
def test_add_order(mock_get, client, db):
    cli1 = Client(**test_client)
    emp = Employee(**test_employee)
    db.bulk_save_objects([cli1, emp])
    db.commit()
    mock_get.json.return_value = {"distance": 1.0}
    response = client.post("/fast_delivery/orders", json=test_order[0])
    assert response.status_code == 200
    assert db.query(Order.distance).filter(Order.id == 1).first()[0] == 1.61
    response = client.post("/fast_delivery/orders", json=test_order[1])
    assert response.status_code == 422


def test_get_orders(client):
    response = client.get("/fast_delivery/orders")
    assert response.status_code == 200


def test_get_orders_with_filters_dates(client):

    date_ = date.today().strftime("%Y-%m-%d")
    response = client.get(f"/fast_delivery/orders?start_date={date_}&end_date={date_}")
    assert response.status_code == 200


def test_get_orders_with_filters_prices(client):

    response = client.get(f"/fast_delivery/orders?start_date=&end_date=&low_price=90&high_price=110&employee=")
    assert response.status_code == 200
    assert b"Wielopole 1" in response.content

@patch("app.routers.utils.requests.get")
def test_get_orders_with_employee_filter(mock_get, client):
    mock_get.json.return_value = {"distance": 1.0}
    client.post("/fast_delivery/orders", json=test_order[2])
    response = client.get(f"/fast_delivery/orders?start_date=&end_date=&low_price=&high_price=&employee=Jack+Track")
    assert response.status_code == 200
    assert b"Jack Track" in response.content


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
    assert db.query(Order).count() == 1
