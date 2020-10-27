from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Text, Date


class Order(Base):

    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=150))
    source_address = Column(String(length=250))
    destination_address = Column(String(length=250))
    date = Column(Date())
    distance = Column(Float)
    other_info = Column(Text(length=300), nullable=True)

    def to_dict(self):
        return {"id": self.id, "full name": self.full_name, "source address": self.source_address,
                "destination address": self.destination_address, "date": self.date}

    def __repr__(self):
        return {"id": self.id, "delivery guy": self.full_name}