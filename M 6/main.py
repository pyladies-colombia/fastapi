from datetime import datetime

from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class ReservationBase(SQLModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None


class Reservation(ReservationBase, table=True):
    id: int = Field(default=None, primary_key=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()


@app.post("/reservations/")
def create_reservation(reservation: ReservationBase):
    with Session(engine) as session:
        db_reservation = Reservation.model_validate(reservation)
        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)
        return db_reservation


@app.get("/reservations/")
def read_reservations():
    with Session(engine) as session:
        reservations = session.exec(select(Reservation)).all()
        return reservations
