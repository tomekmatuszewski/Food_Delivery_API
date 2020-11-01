import pytest
from unittest.mock import patch
from app.database import Database
from app.models import Order, Employee, Client
from app.crud import orders
from sqlalchemy.orm import Session

from app.routers.utils import get_distance

test_db = Database("sqlite://")


@pytest.fixture(name="db", scope="module")
def get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()


test_employee = {
    "first_name": "Joe",
    "last_name": "Doe",
    "gender": "M",
    "date_of_birth": "2000-01-01",
    "address": "Test address",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "id_number": "11111111111",
    "salary": 30000,
}

test_client = {
    "company_name": "Test name",
    "address": "test_address",
    "contact_person": "Test Person",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "tax_identification_number": "567",
    "company_id": "123",
}

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
    employee = Employee(**test_employee)
    client = Client(**test_client)
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