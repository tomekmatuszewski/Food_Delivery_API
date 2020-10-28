from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.employees import Employee
from app.schemas.employee_schema import EmployeeSchema

templates = Jinja2Templates(directory="/templates")
employees = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@employees.post("/employees/add")
async def add_employee(emp_request: EmployeeSchema, db: Session = Depends(get_db)):
    emp_dict = emp_request.dict()
    employee = Employee(**emp_dict)
    db.add(employee)
    db.commit()
    return emp_dict
