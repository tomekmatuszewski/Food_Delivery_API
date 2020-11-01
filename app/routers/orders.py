from pathlib import Path
from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
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
async def get_all_orders(request: Request, db: Session = Depends(get_db)):
    """
    Display all orders from db
    :param request:
    :param db: session of database
    :return:
    """
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
) -> Dict:
    order_dict = order_request.dict()
    order = crud_ord.post_order(order_dict, db)
    background_task.add_task(
        crud_ord.post_order_distance,
        order,
        order_dict,
        db,
    )

    return order.to_dict()


@orders.get("/order/{order_id}/delete")
async def delete_order(order_id: str, db: Session = Depends(get_db),):
    crud_ord.delete_order(order_id, db)
    return RedirectResponse(f"/fast_delivery{orders.url_path_for('get_all_orders')}")
