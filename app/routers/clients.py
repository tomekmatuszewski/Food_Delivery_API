from pathlib import Path
from typing import Dict, Optional

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

    client = crud.post_client(client_dict=client_dict, db=db)
    return client.to_dict()




@clients.get("/clients")
async def get_all_clients(
    request: Request,
    company_name: Optional[str] = None,
    contact_person: Optional[str] = None,
    phone: Optional[str] = None,
    db: Session = Depends(get_db),
):
    if any([company_name, contact_person, phone]):
        clients = crud.filter_clients(db, company_name, contact_person, phone)
    else:
        clients = crud.get_clients(db)
    return templates.TemplateResponse(
        "clients.html",
        context={
            "request": request,
            "clients": clients,
        },
    )


@clients.delete("/clients/{client_id}/delete")
async def delete_client(
    client_id: str,
    db: Session = Depends(get_db),
) -> None:
    crud.delete_client(client_id=client_id, db=db)


@clients.put("/clients/{client_id}/update")
async def update_client(
    client_request: ClientSchema,
    client_id: str,
    db: Session = Depends(get_db),
):
    client_dict = client_request.dict()
    client_updated = crud.update_client(
        client_id=client_id, db=db, client_dict=client_dict
    )
    return client_updated
