from typing import Dict, List

import pytest
from sqlalchemy.orm import Session

from app.crud import employees as filters
from app.database import Database
from app.models import Employee

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
        "first_name": "Joe",
        "last_name": "Doe",
        "gender": "M",
        "date_of_birth": "1990-01-01",
        "address": "Kraków, Raciborska 1",
        "phone": "500-500-500",
        "email": "jd@demo.pl",
        "id_number": "90010115660",
        "salary": 3000,
    },
    {
        "first_name": "Jack",
        "last_name": "Track",
        "gender": "M",
        "date_of_birth": "1991-01-01",
        "address": "Kraków, Kobierzyńska 1",
        "phone": "501-501-501",
        "email": "jdy@demo.pl",
        "id_number": "91010150033",
        "salary": 2000,
    },
]


def populate_db(base: List[Dict], db: Session):
    for emp in base:
        employee = Employee(**emp)
        db.add(employee)
        db.commit()


def test_filter_by_lastname(db):
    populate_db(test_employees, db)
    employee = filters.filter_employees(last_name="Doe", db=db)
    assert len(employee.all()) == 1
    assert employee.all()[0].full_name == "Joe Doe"


def test_filter_by_lastname_non(db):
    employee = filters.filter_employees(last_name="xxx", db=db)
    assert len(employee.all()) == 0


def test_filter_by_phone(db):
    employee = filters.filter_employees(phone="500-500-500", db=db)
    assert len(employee.all()) == 1
    assert employee.all()[0].full_name == "Joe Doe"


def test_filter_by_salary(db):
    employee = filters.filter_employees(max_salary="2100", min_salary="1900", db=db)
    assert len(employee.all()) == 1
    assert employee.all()[0].full_name == "Jack Track"


def test_filter_by_salary_more_than_one(db):
    employee = filters.filter_employees(max_salary="3500", min_salary="1000", db=db)
    assert len(employee.all()) == 2


def test_filter_by_salary_only_min(db):
    employee = filters.filter_employees(min_salary="2500", db=db)
    assert len(employee.all()) == 1


def test_filter_by_salary_only_max(db):
    employee = filters.filter_employees(max_salary="2500", db=db)
    assert len(employee.all()) == 1


def test_filter_by_salary__empty_set(db):
    employee = filters.filter_employees(min_salary="3400", max_salary="4000", db=db)
    assert len(employee.all()) == 0
