from typing import Dict

from sqlalchemy.orm import Query, Session

from app import Employee, schemas


def get_employee(db: Session) -> Query:
    """
    :param db: Session
    :return: Query - all employees
    """
    return db.query(Employee)


def post_employee(emp_dict: Dict, db: Session) -> Employee:
    """
    :param emp_dict:
    :param db:
    :return: added client to db
    """
    employee = Employee(**emp_dict)
    db.add(employee)
    db.commit()
    return employee
