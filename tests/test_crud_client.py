import pytest

from app.database import Database
from app.models import Client
from app.crud import clients
from sqlalchemy.orm import Session

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
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "789",
        "company_id": "456",
    }
]


def populate_db(db: Session):
    client = Client(**test_clients[0])
    db.add(client)
    db.commit()


def test_get_clients(db):
    populate_db(db)
    all_clients = clients.get_clients(db)
    assert all_clients.count() == 1
    assert all_clients.get(1).company_name == "Test name"


def test_post_client(db):
    client = clients.post_client(test_clients[1], db)
    assert db.query(Client).count() == 2
    assert client.to_dict() == {
        "id": 2,
        "company_name": "Test name2",
        "address": "test_address",
        "contact_person": "Test Person",
        "phone": "000-000-000",
        "email": "test@demo.pl",
        "tax_identification_number": "789",
        "company_id": "456",
    }


def test_update_client(db):
    client_upd_dict = {
        "company_name": "Test name22",
        "address": "test_address1",
        "contact_person": "Test Person1",
        "phone": "100-100-000",
        "email": "test1@demo.pl",
        "tax_identification_number": "7891",
        "company_id": "4561",
    }
    client_updated = clients.update_client('1', db, client_upd_dict)
    assert db.query(Client).count() == 2
    assert client_updated == {'address': 'test_address1',
                              'company_id': '4561',
                              'company_name': 'Test name22',
                              'contact_person': 'Test Person1',
                              'email': 'test1@demo.pl',
                              'id': 1,
                              'phone': '100-100-000',
                              'tax_identification_number': '7891'}


def test_delete_client(db):
    clients.delete_client("1", db)
    assert db.query(Client).count() == 1
    assert db.query(Client).filter(Client.id == 2).first().company_name == "Test name2"