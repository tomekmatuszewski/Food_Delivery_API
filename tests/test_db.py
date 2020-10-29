import pytest
from app import database
from app.models import Client


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