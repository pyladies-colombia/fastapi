from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field


class Reservation(BaseModel):
    name: str
    email: str
    datetime: datetime
    guests: int = Field(gt=0, lt=10)
    observation: str | None = None


app = FastAPI()


@app.post("/reservation/")
async def create_reservation(reservation: Reservation):
    return reservation
