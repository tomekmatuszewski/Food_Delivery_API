from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from app import database
from app.routers import orders, employees, clients


app = FastAPI()
BASE_DIR = Path(__file__).parent.parent

app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")

database.init_db()

app.include_router(orders, prefix="/fast_delivery", tags=["orders"])
app.include_router(employees, prefix="/fast_delivery", tags=["employees"])
app.include_router(clients, prefix="/fast_delivery", tags=["clients"])
