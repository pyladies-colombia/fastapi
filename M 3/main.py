
from fastapi import FastAPI, HTTPException

# Inicializa la aplicación FastAPI
app = FastAPI()

# Datos de ejemplo
reservations = [
    {"reservation_id": 1, "name": "Pyladies", "date": "2024-06-01", "num_people": 30},
    {"reservation_id": 2, "name": "alejsdev", "date": "2024-06-02", "num_people": 4},
    {"reservation_id": 3, "name": "tiangolo", "date": "2024-06-03", "num_people": 3},
]

# Define una ruta para obtener una reservación específica por ID
@app.get("/reservations/{reservation_id}")
def get_reservation(reservation_id: int):
    # Itera sobre las reservas para encontrar la que coincide con el ID proporcionado
    for reservation in reservations:
        if reservation["reservation_id"] == reservation_id:
            # Si se encuentra la reservación, la retorna
            return reservation
    # Si no se encuentra la reservación, lanza una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Reservation not found")

# Define una ruta para obtener todas las reservas con un límite opcional
@app.get("/reservations/")
def get_reservations(limit: int | None = None):
    # Si se proporciona un límite, retorna solo ese número de reservas
    if limit:
        return reservations[:limit]
    # Si no se proporciona un límite, retorna todas las reservas
    return reservations