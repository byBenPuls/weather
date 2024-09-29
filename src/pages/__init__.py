from fastapi import APIRouter
from starlette.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="src/pages/static")
