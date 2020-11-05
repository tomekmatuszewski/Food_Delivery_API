from pathlib import Path
from typing import Dict, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import database
from app.crud import clients as crud_cli
from app.crud import employees as crud_emp
from app.crud import orders as crud_ord
from app.schemas import OrderSchema


BASE_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
orders = APIRouter()


def get_db() -> Session:
    global db
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


@orders.get("/orders")
async def get_all_orders(
    request: Request,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    low_price: Optional[str] = None,
    high_price: Optional[str] = None,
    employee: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if any([start_date, end_date, low_price, high_price, employee]):
        orders = crud_ord.filter_orders(
            db, start_date, end_date, low_price, high_price, employee
        )
    else:
        orders = crud_ord.get_orders(db)

    employees = crud_emp.get_employee(db)
    clients = crud_cli.get_clients(db)
    return templates.TemplateResponse(
        "orders.html",
        context={
            "request": request,
            "orders": orders,
            "employees": employees,
            "clients": clients,
        },
    )


@orders.post("/orders")
async def create_order(
    order_request: OrderSchema,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):

    order_dict = order_request.dict()
    order = crud_ord.post_order(order_dict, db)
    background_task.add_task(
        crud_ord.post_order_distance,
        order,
        order_dict,
        db,
    )
    return order.to_dict()



@orders.delete("/orders/{order_id}/delete")
async def delete_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    crud_ord.delete_order(order_id, db)


@orders.put("/orders/{order_id}/update")
async def update_order(
    order_request: OrderSchema,
    order_id: str,
    background_task: BackgroundTasks,
    db: Session = Depends(get_db),
):
    order_dict = order_request.dict()
    order_updated = crud_ord.update_order(
        order_id=order_id, db=db, order_dict=order_dict
    )

    background_task.add_task(
        crud_ord.post_order_distance, order_updated, order_dict, db
    )

    return order_updated.to_dict()
