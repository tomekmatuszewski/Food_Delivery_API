from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import database
from app import Employee
from app.schemas.employee_schema import EmployeeSchema

BASE_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
employees = APIRouter()


def get_db():
    global db
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


@employees.post("/employee/add")
async def add_employee(emp_request: EmployeeSchema, db: Session = Depends(get_db)):
    emp_dict = emp_request.dict()
    employee = Employee(**emp_dict)
    db.add(employee)
    db.commit()
    return emp_dict


@employees.get("/employees")
async def get_all_employees(request: Request, db: Session = Depends(get_db)):
    """
    Display all clients from db
    :param request:
    :param db: session of database
    :return:
    """
    employees = db.query(Employee)
    return templates.TemplateResponse("employees.html", context={
        "request": request,
        "employees": employees,
    })
