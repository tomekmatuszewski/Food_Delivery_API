from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.clients import Client
from app.schemas.client_schema import ClientSchema

templates = Jinja2Templates(directory="/templates")
clients = APIRouter()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@clients.post("/client/add")
async def add_client(client_request: ClientSchema, db: Session = Depends(get_db)):
    client_dict = client_request.dict()
    client = Client(**client_dict)
    db.add(client)
    db.commit()
    return client_dict
