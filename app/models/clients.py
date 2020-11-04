from typing import Dict

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Client(Base):

    __tablename__ = "client"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(150))
    address = Column(String(150))
    contact_person = Column(String(150))
    phone = Column(String(15))
    email = Column(String(150))
    tax_identification_number = Column(String(12), unique=True)
    company_id = Column(String(9), unique=True)

    orders = relationship("Order", back_populates="client")

    def __repr__(self):
        return f"{self.company_name}, address: {self.address}"

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "company_name": self.company_name,
            "address": self.address,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "tax_identification_number": self.tax_identification_number,
            "company_id": self.company_id,
        }
