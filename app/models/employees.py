from typing import Dict

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import column_property, relationship

from app.database import Base


class Employee(Base):

    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(150))
    last_name = Column(String(150))
    gender = Column(String(6))
    date_of_birth = Column(String(150))
    address = Column(String(150))
    phone = Column(String(15))
    email = Column(String(100))
    id_number = Column(String(11), unique=True)
    salary = Column(Float())
    fullname = column_property(first_name + " " + last_name)

    orders = relationship("Order", back_populates="employee")

    @hybrid_property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        return f"{self.full_name}"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
            "id_number": self.id_number,
            "salary": self.salary,
        }
