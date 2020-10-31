import pytest
from app.models import Client, Employee
from app.database import Database

test_db = Database('sqlite://')


@pytest.fixture(name='db')
def get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()


test_client = {"company_name": "Test name",
               "address": "test_address",
               "contact_person": "Test Person",
               "phone": "000-000-000",
               "email": "test@demo.pl",
               "tax_identification_number": "000000000",
               "company_id": "0000"}

test_employee = {"first_name": "Test name",
                 "last_name": "lastname",
                 "gender": "M",
                 "date_of_birth": "2000-01-01",
                 "address": "Test address",
                 "phone": "000-000-000",
                 "email": "test@demo.pl",
                 "id_number": "11111111111",
                 "salary": "30000", }


def test_add_client(db):
    client = Client(**test_client)
    db.add(client)
    db.commit()
    assert db.query(Client).count() == 1
    assert db.query(Client.address).filter(Client.id == 1).first()[0] == 'test_address'


def test_add_employee(db):
    employee = Employee(**test_employee)
    db.add(employee)
    db.commit()
    assert db.query(Employee).count() == 1
    assert db.query(Employee.first_name).filter(Employee.id == 1).first()[0] == "Test name"
    assert employee.full_name == "Test name lastname"
