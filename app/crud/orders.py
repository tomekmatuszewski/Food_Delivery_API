from datetime import date
from typing import Dict

from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app import Client, Employee, Order
from app.database import Base
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


def post_order_distance(order: Order, order_dict: Dict, db: Session) -> None:
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


def filter_orders(
    start_date: str,
    end_date: str,
    low_price: str,
    high_price: str,
    employee: str,
    db: Session,
) -> Order:

    query = db.query(Order)

    if any([start_date, end_date]) and any([low_price, high_price]):
        orders = filter_multiple(
            query, start_date, end_date, low_price, high_price, employee
        )

    elif any([start_date, end_date]):
        orders = filter_by_two_params(query, start_date, end_date, Order.date)

    elif any([low_price, high_price]):
        orders = filter_by_two_params(query, low_price, high_price, Order.full_price)

    else:
        orders = filter_by_employee(query, employee)

    return orders


def filter_by_two_params(
    query: Query, param1: str, param2: str, model_field: InstrumentedAttribute
) -> Base:
    """
    :param query: all objects in table
    :param param1: first param of querystring e.g. -> lowest price
    :param param2: second param of querystring e.g. -> highest price
    :param model_field: table column -> filter param
    :return: filtered query
    """
    if param1 and param2:
        result = query.filter(model_field.between(param1, param2))
    elif not param2:
        result = query.filter(model_field >= param1)
    else:
        result = query.filter(model_field <= param2)

    return result


def filter_multiple(
    query: Query,
    start_date: str,
    end_date: str,
    low_price: str,
    high_price: str,
    employee: str,
) -> Order:

    query_dates = query.filter(Order.date.between(start_date, end_date))
    query_prices = query.filter(Order.full_price.between(low_price, high_price))

    if all([start_date, end_date, low_price, high_price]) and not employee:
        orders = query_dates.filter(Order.full_price.between(low_price, high_price))

    elif all([start_date, end_date, employee]):
        orders = query_dates.join(Employee).filter(Employee.fullname == employee)

    elif all([low_price, high_price, employee]):
        orders = query_prices.join(Employee).filter(Employee.fullname == employee)

    else:
        orders = (
            query_dates.filter(Order.date.between(low_price, high_price))
            .join(Employee)
            .filter(Employee.fullname == employee)
        )

    return orders


def filter_by_employee(query: Query, employee: str) -> Order:
    orders = query.join(Employee).filter(Employee.fullname == employee)
    return orders
