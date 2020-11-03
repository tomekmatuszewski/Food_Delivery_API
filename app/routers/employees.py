from pathlib import Path
from typing import Dict

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

from app import Employee, database
from app.crud import employees as crud
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


@employees.post("/employees")
async def add_employee(
    emp_request: EmployeeSchema, db: Session = Depends(get_db)
) -> Dict:
    emp_dict = emp_request.dict()
    employee = crud.post_employee(emp_dict, db)
    return employee.to_dict()


@employees.get("/employees")
async def get_all_employees(request: Request, db: Session = Depends(get_db)):
    employees = crud.get_employee(db)
    return templates.TemplateResponse(
        "employees.html",
        context={
            "request": request,
            "employees": employees,
        },
    )


@employees.delete("/employees/{emp_id}/delete")
async def delete_employee(emp_id: str, db: Session = Depends(get_db)):
    crud.delete_employee(emp_id, db)


@employees.put("/employees/{emp_id}/update")
async def update_employee(emp_request: EmployeeSchema, emp_id: str, db: Session = Depends(get_db)):
    emp_dict = emp_request.dict()
    emp_updated = crud.update_employee(emp_id=emp_id, db=db, emp_dict=emp_dict)
    return emp_updated

