from pathlib import Path
from typing import Dict

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import database
from app.crud import clients as crud
from app.schemas.client_schema import ClientSchema

BASE_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
clients = APIRouter()


def get_db() -> Session:
    global db
    try:
        db = database.SessionLocal()
        yield db
    finally:
        db.close()


@clients.post("/clients")
async def add_client(
    client_request: ClientSchema, db: Session = Depends(get_db)
) -> Dict:
    client_dict = client_request.dict()
    client = crud.post_client(client_dict, db)
    return client.to_dict()


@clients.get("/clients")
async def get_all_clients(request: Request, db: Session = Depends(get_db)):
    clients = crud.get_clients(db)
    return templates.TemplateResponse(
        "clients.html",
        context={
            "request": request,
            "clients": clients,
        },
    )
