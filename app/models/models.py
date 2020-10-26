from app.database import Base
from sqlalchemy import Column, Integer, String, Float, Text, Date


class Order(Base):

    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(length=150))
    price = Column(Float)
    source_address = Column(String(length=250))
    destination_address = Column(String(length=250))
    date = Column(Date())
    other_info = Column(Text(length=300), nullable=True)


