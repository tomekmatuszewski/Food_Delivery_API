from datetime import date
from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Client, Order
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