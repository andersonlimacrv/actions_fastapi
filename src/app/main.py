import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from src.app.exceptions.exceptions import (
    UsernameAlreadyExists,
    create_exception_handler,
)
from src.app.api.v1 import api_router
from src.app.backend_pre_start import async_main

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


async def startup_event():
    await async_main()


app.add_event_handler("startup", startup_event)


app.add_exception_handler(
    exc_class_or_status_code=UsernameAlreadyExists,
    handler=create_exception_handler(
        status_code=status.HTTP_400_BAD_REQUEST,
        initial_detail="Data can't be processed, check the input.",
    ),
)


def start():
    """Iniciado com 'poetry run start' no nível raiz."""
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == "__main__":
    start()
