from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.clients import Client
from app.models.employees import Employee


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    client_id = Column(Integer, ForeignKey("client.id"))
    destination_address = Column(String(length=250))
    contact_phone = Column(String(15))
    date = Column(String(20))
    distance = Column(Float)
    full_price = Column(Float)
    other_info = Column(Text(length=300), nullable=True)

    employee = relationship("Employee", back_populates="orders")
    client = relationship("Client", back_populates="orders")

    def __repr__(self):
        return f"id: {self.id}, delivery person: {self.employee.full_name}," \
               f"client: {self.client.company_name}"

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "client_id": self.client_id,
            "destination_address": self.destination_address,
            "contact_phone": self.contact_phone,
            "date": self.date,
            "distance": self.distance,
            "full_price": self.full_price,
            "other_info": self.other_info,
        }
