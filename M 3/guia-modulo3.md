# Modulo 3 Proyecto: Gestión de Reservas de Mesas en un Restaurante

### Creadora: Johana Alarcón

## Descripción

Este proyecto consiste en una API para gestionar reservas de mesas en un restaurante utilizando FastAPI. La API permite realizar operaciones CRUD (Crear, Leer, Actualizar, Borrar) sobre las reservas.

¿ Estás Lista ? ⚡️

## Requisitos

- Python 3.9+
- FastAPI
- Uvicorn
- SQLAlchemy

## Instalación

### Paso 1: Configuración del Entorno

Primero, asegúrate de tener Python instalado. Luego, crea un entorno virtual e instala FastAPI y Uvicorn.

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

# Instalar FastAPI y Uvicorn
pip install fastapi uvicorn sqlalchemy pydantic
```

### Paso 2: Crear la Estructura del Proyecto

Crea la siguiente estructura de directorios y archivos para el proyecto:

```bash
restaurant_reservation/
│
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
└── requirements.txt
```

### Paso 3:  Configurar la Base de Datos

Configura la conexión a la base de datos usando SQLAlchemy con SQLite.

database.py
```bash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Crear una sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear una base declarativa
Base = declarative_base()
```

### Paso 4:  Crear los Modelos

Define los modelos de la base de datos. En este caso, definimos el modelo para las reservas.

models.py
```bash
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

# Modelo de reserva
class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    date = Column(DateTime)
    num_people = Column(Integer)
```
### Paso 5:  Crear los Esquemas

Define los esquemas para validar las solicitudes y respuestas utilizando Pydantic.

schemas.py
```bash
from pydantic import BaseModel, Field
from datetime import datetime

# Esquema base de reserva
class ReservationBase(BaseModel):
    name: str
    date: datetime
    num_people: int = Field(..., gt=0, description="El número de personas debe ser mayor que 0")

# Esquema para crear una reserva
class ReservationCreate(ReservationBase):
    pass

# Esquema para actualizar una reserva
class ReservationUpdate(ReservationBase):
    pass

# Esquema para leer una reserva, incluyendo el ID
class Reservation(ReservationBase):
    id: int

    class Config:
        orm_mode = True

```
### Paso 6:  Crear Operaciones CRUD

Define las operaciones CRUD (Crear, Leer, Actualizar, Borrar) utilizando SQLAlchemy.

crud.py
```bash
from sqlalchemy.orm import Session
import models, schemas

# Obtener una reserva por ID
def get_reservation(db: Session, reservation_id: int):
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

# Obtener todas las reservas con paginación
def get_reservations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Reservation).offset(skip).limit(limit).all()

# Crear una nueva reserva
def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    db_reservation = models.Reservation(**reservation.dict())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Actualizar una reserva existente
def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationUpdate):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        return None
    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Borrar una reserva
def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    db.delete(db_reservation)
    db.commit()
    return db_reservation

```
### Paso 7:  Crear los Endpoints

Define los endpoints de la API utilizando FastAPI.

main.py
```bash
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

# Crear las tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Dependencia de sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para crear una reserva
@app.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return crud.create_reservation(db=db, reservation=reservation)

# Endpoint para obtener todas las reservas
@app.get("/reservations/", response_model=list[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = crud.get_reservations(db, skip=skip, limit=limit)
    return reservations

# Endpoint para obtener una reserva por ID
@app.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = crud.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

# Endpoint para actualizar una reserva por ID
@app.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: int, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = crud.update_reservation(db, reservation_id=reservation_id, reservation=reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

# Endpoint para borrar una reserva por ID
@app.delete("/reservations/{reservation_id}", response_model=schemas.Reservation)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    return crud.delete_reservation(db, reservation_id=reservation_id)

```

### Paso 8:   Ejecutar la Aplicación

Ejecuta la aplicación con Uvicorn.

```bash
uvicorn main:app --reload
```

### Paso 9:   Probar la API desde Swagger

1. Abre tu navegador web y ve a http://127.0.0.1:8000/docs.
2. Usa los botones "Try it out" en cada endpoint para interactuar con la API:
   
- POST /reservations/ para crear una reserva.
- GET /reservations/ para listar reservas.
- GET /reservations/{reservation_id} para obtener una reserva específica.
- PUT /reservations/{reservation_id} para actualizar una reserva específica.
- DELETE /reservations/{reservation_id} para eliminar una reserva específica.
