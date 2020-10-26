from app.database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    price = Column(Float)

    product_items = relationship("ProductItem", back_populates="product")

    def __repr__(self):
        return f"{self.name}"


class ProductItem(Base):

    __tablename__ = "product_item"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)

    product = relationship("Product", back_populates="product_items")

    def __repr__(self):
        return f"{self.id} {self.product.name}- {self.quantity}"

    @hybrid_property
    def full_price(self):
        return self.quantity * self.product.price


