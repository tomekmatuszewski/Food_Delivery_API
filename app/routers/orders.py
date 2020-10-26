from fastapi import APIRouter
from app.database import SessionLocal
from app.models.models import Order
from sqlalchemy.orm import Session
from fastapi import Depends
from app.schemas.order_schemas import OrderSchema
from datetime import date
orders = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@orders.post("/order")
async def create_item(order_request: OrderSchema, db: Session = Depends(get_db)):
    order_dict = order_request.dict()
    order = Order(**order_dict)
    order.date = date.today()
    db.add(order)
    db.commit()
    return order_dict
