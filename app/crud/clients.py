from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Client


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


def filter_clients(
    db: Session, company_name: str = None, contact_person: str = None, phone: str = None
) -> Query:
    clients = db.query(Client)
    if company_name:
        return clients.filter(Client.company_name.like(f"%{company_name}%"))
    elif contact_person:
        return clients.filter(Client.contact_person.like(f"%{contact_person}%"))
    else:
        return clients.filter(Client.phone == phone)
