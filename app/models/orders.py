from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models.employees import Employee
from app.models.clients import Client
from app.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    client_id = Column(Integer, ForeignKey("client.id"))
    destination_address = Column(String(length=250))
    date = Column(Date())
    distance = Column(Float)
    full_price = Column(Float)
    other_info = Column(Text(length=300), nullable=True)

    employee = relationship("Employee", back_populates="orders")
    client = relationship("Client", back_populates="orders")

    def __repr__(self):
        return {"id": self.id, "delivery person": self.employee.full_name, "client": self.client.company_name}
