from datetime import date
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.main import database
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
    return templates.TemplateResponse("home.html", context={
        "request": request,
        "orders": orders,
        "employees": employees,
        "clients": clients,
    })


def add_distance(order: Order, db: Session, client_id, destination_address):
    client_address = db.query(Client).get(client_id).address
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

    db.add(order)
    db.commit()
    background_task.add_task(
        add_distance,
        order,
        db,
        order_request.client_id,
        order_request.destination_address,
    )

    return order_dict
