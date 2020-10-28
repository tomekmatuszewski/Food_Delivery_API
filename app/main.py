from fastapi import FastAPI

from app.database import Base, engine
from app.routers.orders import orders
from app.routers.employees import employees

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(orders, prefix="/fast_delivery", tags=["orders"])
app.include_router(employees, prefix="/fast_delivery", tags=["employees"])
