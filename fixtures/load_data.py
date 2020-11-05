from pathlib import Path
import json
from sqlalchemy.orm import Session
from app import Employee, Client, Order
from app.routers.utils import get_distance
from datetime import date

BASE_DIR = Path(__file__).parent.parent


def load_fixtures(db: Session) -> None:
    with open(f"{BASE_DIR}/fixtures/db_data.json") as json_file:
        data_dict = json.load(json_file)

        for employee in data_dict["employees"]:
            db.add(Employee(**employee))
            db.commit()

        for client in data_dict["clients"]:
            db.add(Client(**client))
            db.commit()

        for order in data_dict["orders"]:
            ord = Order(**order)
            ord.date = date.today()
            address_from = db.query(Client).get(order["client_id"]).address
            ord.distance = get_distance(address_from=address_from, address_to=order["destination_address"])
            db.add(ord)
            db.commit()





