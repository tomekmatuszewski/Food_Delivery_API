from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employee.id"))
    source_address = Column(String(length=250))
    destination_address = Column(String(length=250))
    date = Column(Date())
    distance = Column(Float)
    other_info = Column(Text(length=300), nullable=True)

    employee = relationship("Employee", back_populates="orders")

    def to_dict(self):
        return {
            "id": self.id,
            "source address": self.source_address,
            "destination address": self.destination_address,
            "distance": self.distance,
            "date": self.date,
        }

    def __repr__(self):
        return {"id": self.id, "delivery person": self.employee.full_name}
