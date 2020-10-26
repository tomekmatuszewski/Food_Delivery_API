from fastapi import FastAPI
from app.routers.orders import orders
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(orders, prefix="/fastfood", tags=["orders"])

