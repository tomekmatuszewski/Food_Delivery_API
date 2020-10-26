from fastapi import APIRouter
from app.database import SessionLocal
from app.models.orders import Order
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.order_schemas import OrderSchema
from datetime import date
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="/templates")
orders = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@orders.get("/orders")
async def get_all_orders(db: Session = Depends(get_db)):
    """
    Display all orders from db
    :param db:
    :return:
    """
    orders = db.query(Order).all()
    return [order.to_dict() for order in orders]


@orders.post("/orders")
async def create_order(order_request: OrderSchema, db: Session = Depends(get_db)):
    order_dict = order_request.dict()
    order = Order(**order_dict)
    order.date = date.today()
    db.add(order)
    db.commit()
    return order_dict
