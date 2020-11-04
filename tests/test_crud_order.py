from datetime import date
from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from app.crud import orders
from app.database import Database
from app.models import Client, Employee, Order
from app.routers.utils import get_distance

test_db = Database("sqlite://")


@pytest.fixture(name="db", scope="module")
def get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()


test_employee = [
    {
        "first_name": "Joe",
        "last_name": "Doe",
        "gender": "M",
        "date_of_birth": "2000-01-01",
        "address": "Test address",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "id_number": "11111111111",
        "salary": 3000,
    },
    {
        "first_name": "Jack",
        "last_name": "Doey",
        "gender": "M",
        "date_of_birth": "1990-01-01",
        "address": "Test address1",
        "phone": "500-900-100",
        "email": "test1@demo.pl",
        "id_number": "5454",
        "salary": 2000,
    },
]

test_client = [
    {
        "company_name": "Test name",
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "567",
        "company_id": "123",
    },
    {
        "company_name": "Test name2",
        "address": "test_address2",
        "contact_person": "Test Person2",
        "phone": "100-100-100",
        "email": "test1@demo.pl",
        "tax_identification_number": "111",
        "company_id": "222",
    },
]

test_orders = [
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
        "contact_phone": "530-000-000",
        "destination_address": "Kraków, Wielopole 2",
        "full_price": 100,
    },
]


def populate_db(db: Session):
    employee = Employee(**test_employee[0])
    client = Client(**test_client[0])
    order = Order(**test_orders[0])
    db.bulk_save_objects([employee, client, order])
    db.commit()


def test_get_employees(db):
    populate_db(db)
    all_orders = orders.get_orders(db)
    assert all_orders.count() == 1
    assert all_orders.get(1).destination_address == "Kraków, Wielopole 1"


def test_post_order(db):
    order = orders.post_order(test_orders[1], db)
    assert db.query(Order).count() == 2
    assert repr(order) == "id: 2, delivery person: Joe Doe,client: Test name"


@patch("app.routers.utils.requests.get")
def test_get_distance(mock_get):
    mock_get.json.return_value = {"distance": 1.0}
    value = get_distance("Test address", "Test_address")
    assert value == 1.61


@patch("app.routers.utils.requests.get")
def test_post_order_distance(mock_get, db):
    mock_get.json.return_value = {"distance": 1.0}
    order = db.query(Order).get(2)
    orders.post_order_distance(order, test_orders[1], db)
    assert db.query(Order.distance).filter(Order.id == 2).first()[0] == 1.61


def test_update_order(db):
    order_updated_dict = {
        "employee_id": 2,
        "client_id": 2,
        "contact_phone": "530-100-000",
        "destination_address": "Kraków, Wielopole 10",
        "full_price": 160,
    }
    order_updated = orders.update_order("2", db, order_updated_dict)
    assert db.query(Order).count() == 2
    assert order_updated.to_dict() == {
        "client_id": 2,
        "contact_phone": "530-100-000",
        "date": date.today(),
        "destination_address": "Kraków, Wielopole 10",
        "distance": 1.61,
        "employee_id": 2,
        "full_price": 160.0,
        "id": 2,
        "other_info": None,
    }


def test_delete_client(db):
    orders.delete_order("1", db)
    assert db.query(Order).count() == 1
    assert db.query(Order).filter_by(id=2).first().client_id == 2
