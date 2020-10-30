import pytest
from app import database
from app.models import Client, Employee


@pytest.fixture(name='db')
def get_db():
    database.init_db('sqlite://')
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


def test_add_client(db):
    client_test = {
        'company_name': "Test name",
        'address': 'Test address'
    }
    client = Client(**client_test)
    db.add(client)
    db.commit()
    assert db.query(Client).count() == 1
    assert db.query(Client.address).filter(Client.id == 1).first()[0] == 'Test address'


def test_add_employee(db):
    emp_test = {
        'first_name': "John",
        'last_name': "Doe"
    }
    employee = Employee(**emp_test)
    db.add(employee)
    db.commit()
    assert db.query(Employee).count() == 1
    assert db.query(Employee.first_name).filter(Employee.id == 1).first()[0] == "John"
    assert employee.full_name == "John Doe"