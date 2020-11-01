import pytest

from app.database import Database
from app.models import Employee
from app.crud import employees
from sqlalchemy.orm import Session

test_db = Database("sqlite://")


@pytest.fixture(name="db", scope="module")
def get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()


test_employees = [
    {
    "first_name": "Test name",
    "last_name": "lastname",
    "gender": "M",
    "date_of_birth": "2000-01-01",
    "address": "Test address",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "id_number": "11111111111",
    "salary": 30000,
    },
    {
    "first_name": "Test name",
    "last_name": "lastname",
    "gender": "M",
    "date_of_birth": "2000-01-01",
    "address": "Test address",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "id_number": "777",
    "salary": 30000,
    }
]


def populate_db(db: Session):
    employee = Employee(**test_employees[0])
    db.add(employee)
    db.commit()


def test_get_employees(db):
    populate_db(db)
    all_employees = employees.get_employee(db)
    assert all_employees.count() == 1
    assert all_employees.get(1).last_name == "lastname"


def test_post_employee(db):
    employee = employees.post_employee(test_employees[1], db)
    assert db.query(Employee).count() == 2
    assert employee.to_dict() == {
    "id": 2,
    "first_name": "Test name",
    "last_name": "lastname",
    "gender": "M",
    "date_of_birth": "2000-01-01",
    "address": "Test address",
    "phone": "000-000-000",
    "email": "test@demo.pl",
    "id_number": "777",
    "salary": 30000,
    }