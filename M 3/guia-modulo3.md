# Modulo 3 Proyecto: Gestión Básica de Reservas

### Creadora: Johana Alarcón

## Descripción

Este proyecto es una API sencilla para gestionar reservas de mesas en un restaurante. Incluye endpoints para obtener una reserva por ID y obtener todas las reservas, con la opción de limitar el número de resultados usando un parámetro de consulta (limit). Este proyecto trabaja con datos de ejemplo estáticos.

¿Estás Lista? ⚡️

## ¿Qué es un Endpoint?

Un endpoint es una URL específica en una API que actúa como un punto de acceso para realizar acciones como obtener, enviar, actualizar o eliminar datos en un sistema. Utiliza métodos HTTP (como GET, POST, PUT, DELETE) y puede recibir parámetros para especificar detalles adicionales.

## Manos a la Obra

### Paso 1: Requerimientos

Asegúrate de tener los requerimientos indicados en el [Módulo 2](../M%202/guia-modulo2.md)

### Paso 2: Crear la Estructura del Proyecto

Crea la siguiente estructura de directorios y archivos para el proyecto:

```bash
restaurant_reservation/
├── main.py
```

### Paso 3:  Crear los Endpoints

Define una aplicación FastAPI con rutas para obtener una reservación específica por ID, y para listar todas las reservaciones con un límite opcional.

*main.py*
```python
from fastapi import FastAPI, HTTPException
from typing import List, Optional

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
    # Itera sobre las reservaciones para encontrar la que coincide con el ID proporcionado
    for reservation in reservations:
        if reservation["reservation_id"] == reservation_id:
            # Si se encuentra la reservación, la retorna
            return reservation
    # Si no se encuentra la reservación, lanza una excepción HTTP 404
    raise HTTPException(status_code=404, detail="Reservation not found")

# Define una ruta para obtener todas las reservaciones con un límite opcional
@app.get("/reservations/")
def get_reservations(limit: Union[int, None] = None):
    # Si se proporciona un límite, retorna solo ese número de reservaciones
    if limit:
        return reservations[:limit]
    # Si no se proporciona un límite, retorna todas las reservaciones
    return reservations

```

### Paso 4:   Ejecutar la Aplicación

Ejecuta la aplicación con FastAPI.

```bash
fastapi dev main.py
```

### Paso 5:   Probar la API desde Swagger

1. Abre tu navegador web y ve a http://127.0.0.1:8000/docs.
2. Usa los botones "Try it out" en cada endpoint para interactuar con la API:
    - GET /reservations/{reservation_id} para obtener una
    - GET /reservations/ para listar reservas.


Ejemplo:
- Visualización de los endpoints en Swagger UI.
![](./images/image_1.png)
- Despliegue de la sección y clic en el botón "Try it out".
![](./images/image_2.png)
- Prueba de GET.
![](./images/image_3.png)


## Aceptas un Reto 🤓

Dentro de la función `get_reservation`, agrega una validación para verificar que el `reservation_id` proporcionado sea un número positivo.