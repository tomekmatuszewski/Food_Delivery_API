from datetime import date
from pathlib import Path
from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.orders import Order
from app.models.employees import Employee
from app.routers.utils import get_distance
from app.schemas.order_schemas import OrderSchema

BASE_DIR = Path(__name__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
orders = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@orders.get("/orders")
async def get_all_orders(request: Request, db: Session = Depends(get_db)):
    """
    Display all orders from db
    :param db:
    :return:
    """
    orders = db.query(Order)
    employees = db.query(Employee)
    return templates.TemplateResponse("home.html", context={
        "request": request,
        "orders": orders,
        "employees": employees
    })


def add_distance(order: Order, db: Session, source_address, destination_address):
    distance = get_distance(source_address, destination_address)
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
        order_request.source_address,
        order_request.destination_address,
    )

    return order_dict
