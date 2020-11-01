from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/templates")
home = APIRouter()


@home.get("/")
async def get_home(request: Request):

    return templates.TemplateResponse(
        "home.html",
        context={
            "request": request,
        },
    )
