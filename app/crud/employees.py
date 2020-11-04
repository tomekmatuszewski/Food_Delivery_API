from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Employee


def get_employee(db: Session) -> Query:
    return db.query(Employee)


def post_employee(emp_dict: Dict, db: Session) -> Employee:
    employee = Employee(**emp_dict)
    db.add(employee)
    db.commit()
    return employee


def delete_employee(employee_id: str, db: Session) -> None:
    employee = db.query(Employee).get(employee_id)
    db.delete(employee)
    db.commit()


def update_employee(emp_id: str, db: Session, emp_dict: Dict) -> Dict:
    emp_query = db.query(Employee).filter(Employee.id == emp_id)
    emp_query.update(emp_dict)
    emp_updated = db.query(Employee).filter_by(id=emp_id).first()
    db.commit()
    return emp_updated.to_dict()


def filer_employees(
    last_name: str, phone: str, min_salary: str, max_salary: str, db: Session
) -> Employee:
    query = db.query(Employee)
    if last_name:
        employees = query.filter(Employee.last_name.like(f"%{last_name}%"))
    elif phone:
        employees = query.filter(Employee.phone == phone)
    else:
        employees = filter_by_salary(query, min_salary, max_salary)
    return employees


def filter_by_salary(query: Query, min_salary: str, max_salary: str) -> Employee:

    if min_salary and max_salary:
        result = query.filter(Employee.salary.between(min_salary, max_salary))
    elif not max_salary:
        result = query.filter(Employee.salary >= min_salary)
    else:
        result = query.filter(Employee.salary <= max_salary)

    return result
