from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Client, schemas


def get_clients(db: Session) -> Query:
    """

    :param db: Session
    :return: Query - all companies - clients
    """
    return db.query(Client)


def post_client(client_dict: Dict, db: Session) -> Client:
    """

    :param client_dict: json response converted to dict
    :param db:
    :return: added client to db
    """
    client = Client(**client_dict)
    db.add(client)
    db.commit()
    return client


def delete_client(client_id: str, db: Session) -> None:
    client = db.query(Client).get(client_id)
    db.delete(client)
    db.commit()


def update_client(client_id: str, db: Session, client_dict: Dict) -> Dict:
    client_query = db.query(Client).filter(Client.id == client_id)
    client_query.update(client_dict)
    client_updated = db.query(Client).filter_by(id=client_id).first()
    db.commit()
    return client_updated.to_dict()


