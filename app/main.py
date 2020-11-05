from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).parent.parent


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


app.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")

from app import routers

app.include_router(routers.orders, prefix="/fast_delivery", tags=["orders"])
app.include_router(routers.employees, prefix="/fast_delivery", tags=["employees"])
app.include_router(routers.clients, prefix="/fast_delivery", tags=["clients"])
app.include_router(routers.home, prefix="/fast_delivery")
