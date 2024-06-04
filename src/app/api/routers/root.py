from fastapi import APIRouter, status

from src.app.schemas.message import Message

router = APIRouter(tags=["Hello World Route 🔥 "])


@router.get("/", status_code=status.HTTP_200_OK, response_model=Message)
async def read_root():
    return {"message": "Olá Mundo!"}
