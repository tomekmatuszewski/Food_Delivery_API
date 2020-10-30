from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent


def create_app():
    app = FastAPI()

    app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")

    from app import routers

    app.include_router(routers.orders, prefix="/fast_delivery", tags=["orders"])
    app.include_router(routers.employees, prefix="/fast_delivery", tags=["employees"])
    app.include_router(routers.clients, prefix="/fast_delivery", tags=["clients"])

    return app
