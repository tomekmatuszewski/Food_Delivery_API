from datetime import date
from datetime import datetime
from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Client, Order, Employee
from app.routers.utils import get_distance


def get_orders(db: Session) -> Query:
    """

    :param db: Session
    :return: Query - all companies - clients
    """
    return db.query(Order)


def post_order(order_dict: Dict, db: Session) -> Order:
    """
    :param order_dict: request converted to dict
    :param db: session
    :return: added client to db
    """
    order = Order(**order_dict)
    order.date = date.today()
    db.add(order)
    db.commit()
    return order


def post_order_distance(
        order: Order, order_dict: Dict, db: Session
) -> None:
    client_address = db.query(Client).get(order_dict["client_id"]).address
    distance = get_distance(client_address, order_dict["destination_address"])
    order.distance = distance
    db.add(order)
    db.commit()


def delete_order(order_id: str, db: Session) -> None:
    order = db.query(Order).get(order_id)
    db.delete(order)
    db.commit()


def update_order(order_id: str, db: Session, order_dict: Dict) -> Order:
    order_query = db.query(Order).filter(Order.id == order_id)
    order_query.update(order_dict)
    order_updated = db.query(Order).filter_by(id=order_id).first()
    db.commit()
    return order_updated


def filter_orders(start_date: str, end_date: str, low_price: str, high_price: str, employee: str, db: Session) -> Order:
    if all([start_date, end_date, low_price, high_price, employee]):
        orders = filer_all_fields(start_date, end_date, low_price, high_price, employee, db)
    elif any([start_date, end_date]) and not all([low_price, high_price, employee]):
        orders = filter_by_dates(start_date, end_date, db)
    elif any([low_price, high_price]) and not all([start_date, end_date, employee]):
        orders = filter_by_prices(low_price, high_price, db)
    else:
        orders = filter_by_employee(employee, db)
    return orders


def filer_all_fields(start_date: str, end_date: str, low_price: str, high_price: str, employee: str, db: Session) -> Order:
    orders = db.query(Order).filter(Order.date.between(start_date, end_date)).\
        filter(Order.full_price.between(low_price, high_price)).join(Employee).filter(Employee.fullname == employee)
    return orders


def filter_by_dates(start_date: str, end_date: str, db: Session) -> Order:
    if start_date and end_date:
        orders = db.query(Order).filter(Order.date.between(start_date, end_date))
    elif start_date and not end_date:
        orders = db.query(Order).filter(Order.date >= start_date)
    else:
        orders = db.query(Order).filter(Order.date <= end_date)
    return orders


def filter_by_prices(low_price, high_price, db: Session) -> Order:
    if low_price and high_price:
        orders = db.query(Order).filter(Order.full_price.between(low_price, high_price))
    elif low_price and not high_price:
        orders = db.query(Order).filter(Order.full_price >= low_price)
    else:
        orders = db.query(Order).filter(Order.full_price <= high_price)
    return orders


def filter_by_employee(employee: str, db) -> Order:
    orders = db.query(Order).join(Employee).filter(Employee.fullname == employee)
    return orders

