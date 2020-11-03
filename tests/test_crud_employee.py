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


def test_update_employee(db):
    employee_upd_dict = {
        "first_name": "Test name1",
        "last_name": "lastname1",
        "gender": "F",
        "date_of_birth": "1990-01-01",
        "address": "Test address1",
        "phone": "500-000-000",
        "email": "test1@demo.pl",
        "id_number": "69000",
        "salary": 2000,
    }
    emp_updated = employees.update_employee('1', db, employee_upd_dict)
    assert db.query(Employee).count() == 2
    assert emp_updated == {'address': 'Test address1',
                           'date_of_birth': '1990-01-01',
                           'email': 'test1@demo.pl',
                           'first_name': 'Test name1',
                           'gender': 'F',
                           'id': 1,
                           'id_number': '69000',
                           'last_name': 'lastname1',
                           'phone': '500-000-000',
                           'salary': 2000.0}


def test_delete_client(db):
    employees.delete_employee("1", db)
    assert db.query(Employee).count() == 1
    assert db.query(Employee).filter(Employee.id == 2).first().first_name == "Test name"
