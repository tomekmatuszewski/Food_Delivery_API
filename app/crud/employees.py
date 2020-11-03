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
