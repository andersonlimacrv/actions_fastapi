import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World from deploy"}


def start():
    """Launched with 'poetry run start' at root level."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8888, reload=True)
