from datetime import date
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import database
from app.models import Client, Employee, Order
from app.routers.utils import get_distance
from app.schemas import OrderSchema

BASE_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
orders = APIRouter()


def get_db():
    global db
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


@orders.get("/orders")
async def get_all_orders(request: Request, db: Session = Depends(get_db)):
    """
    Display all orders from db
    :param request:
    :param db: session of database
    :return:
    """
    orders = db.query(Order)
    employees = db.query(Employee)
    clients = db.query(Client)
    return templates.TemplateResponse("orders.html", context={
        "request": request,
        "orders": orders,
        "employees": employees,
        "clients": clients,
    })


def add_distance(order: Order, client_address: str, db: Session, destination_address):

    distance = get_distance(client_address, destination_address)
    order.distance = distance
    db.add(order)
    db.commit()


@orders.post("/orders")
async def create_order(
    order_request: OrderSchema,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order_dict = order_request.dict()
    order = Order(**order_dict)
    order.date = date.today()
    client_address = db.query(Client).get(order_request.client_id).address
    db.add(order)
    db.commit()
    background_task.add_task(
        add_distance,
        order,
        client_address,
        db,
        order_request.destination_address,
    )

    return order_dict



