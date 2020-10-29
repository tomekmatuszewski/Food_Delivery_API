from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Client(Base):

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150))
    address = Column(String(150))

    orders = relationship("Order", back_populates="client")

    def __repr__(self):
        return f"{self.company_name}, address: {self.address}"
