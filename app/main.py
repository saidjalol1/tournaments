from fastapi import FastAPI
from app.api.v1 import tournament

app = FastAPI()

app.include_router(tournament.router)
