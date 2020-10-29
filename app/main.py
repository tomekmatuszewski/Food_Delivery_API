from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import orders, employees, clients

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)

app.include_router(orders, prefix="/fast_delivery", tags=["orders"])
app.include_router(employees, prefix="/fast_delivery", tags=["employees"])
app.include_router(clients, prefix="/fast_delivery", tags=["clients"])
