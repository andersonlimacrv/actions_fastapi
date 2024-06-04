import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.api.main import api_router
from src.app.backend_pre_start import async_main

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


async def startup_event():
    await async_main()


app.add_event_handler("startup", startup_event)


def start():
    """Iniciado com 'poetry run start' no nível raiz."""
    uvicorn.run("src.app.main:app", host="0.0.0.0", port=8888, reload=True)


if __name__ == "__main__":
    start()
