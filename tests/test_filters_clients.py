import pytest
from sqlalchemy.orm import Session
from typing import List, Dict
from app.crud import clients as filters
from app.database import Database
from app.models import Client

test_db = Database("sqlite://")


@pytest.fixture(name="db", scope="module")
def get_db():
    try:
        db = test_db.SessionLocal()
        yield db
    finally:
        db.close()



test_clients = [
    {
        "company_name": "Food Company",
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "567",
        "company_id": "123",
    },
    {
        "company_name": "Restaurant",
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "500-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "789",
        "company_id": "456",
    },
]


def populate_db(base: List[Dict], db: Session):
    for item in base:
        client = Client(**item)
        db.add(client)
        db.commit()


def test_filter_by_company_name(db):
    populate_db(test_clients, db)
    client = filters.filter_clients(db=db, company_name="Restaurant")
    assert len(client.all()) == 1
    assert client.all()[0].company_name == "Restaurant"


def test_filter_by_company_name_non_object(db):
    client = filters.filter_clients(db=db, company_name="xxxxx")
    assert len(client.all()) == 0


def test_filter_by_contact_person(db):
    client = filters.filter_clients(db=db, contact_person="Test Person")
    assert len(client.all()) == 2
    assert client.all()[0].contact_person == "Test Person"


def test_filter_by_phone(db):
    client = filters.filter_clients(db=db, phone="500-000-000")
    assert len(client.all()) == 1
    assert client.all()[0].company_name == "Restaurant"