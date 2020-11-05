import pytest
from sqlalchemy.orm import Session
from typing import List, Dict
from app.crud import orders as filters
from app.database import Database
from app.models import Order, Employee
from datetime import date

test_db = Database("sqlite://")

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


test_orders = [
    {
        "employee_id": 1,
        "client_id": 1,
        "date": date(2020, 9, 10),
        "contact_phone": "000-000-000",
        "destination_address": "Kraków, Wielopole 1",
        "full_price": 150,
    },
    {
        "employee_id": 2,
        "client_id": 2,
        "date": date(2020, 10, 10),
        "contact_phone": "530-000-000",
        "destination_address": "Kraków, Wielopole 2",
        "full_price": 100,
    },
]


def populate_db(emp: List[Dict], orders: List[Dict], db: Session):
    for item1, item2 in zip(emp, orders):
        employee = Employee(**item1)
        order = Order(**item2)
        db.add(employee)
        db.add(order)
        db.commit()


@pytest.fixture(name="db", scope="module")
def get_db():
    try:
        db = test_db.SessionLocal()
        populate_db(test_employees, test_orders, db)
        yield db
    finally:
        db.close()


@pytest.mark.parametrize('start_date,end_date,low_price,high_price,employee,expected',
                        (
                                ("2020-10-1", "2020-10-11", None, None, None, 1),
                                ("2020-10-1", None, None, None, None, 1),
                                (None, "2020-10-10", None, None, None, 2),
                                ('2020-08-01', '2020-08-20', None, None, None, 0),
                                (None, None, 140, 160, None, 1),
                                (None, None, None, 160, None, 2),
                                (None, None, 100, None, None, 2),
                                (None, None, 10, 20, None, 0),
                                ('2020-09-01', '2020-09-30', 140, 160, None, 1),
                                ('2020-09-01', '2020-09-30', 80, 90, None, 0),
                                ('2020-09-01', '2020-09-30', None, None, "Joe Doe", 1),
                                (None, None, 90, 110, "Jack Track", 1),
                                (None, None, None, None, "Jack Track", 1),
                                (None, None, None, None, "Jack One", 0),

                        ))
def test_filters_orders(start_date, end_date, low_price, high_price, employee, db, expected):

    orders = filters.filter_orders(db, start_date=start_date, end_date=end_date, low_price=low_price,
                                   high_price=high_price, employee=employee)
    assert len(orders.all()) == expected



