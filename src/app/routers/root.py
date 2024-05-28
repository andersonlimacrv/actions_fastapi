from fastapi import APIRouter
from http import HTTPStatus

from src.app.schemas.message import Message

router = APIRouter(tags=["Hello World Route 🔥 "])


@router.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}
