# Importar librerías
from fastapi import FastAPI

# Crear instancia de FastAPI

# Este será el punto de partida para crear la app
app = FastAPI()

#Crear endpoint

#Definir una ruta de tipo GET en el endpoint raíz ("/")
@app.get("/")
# Definir una función asíncrona que maneja las solicitudes a este endpoint
async def root():
    # La función devuelve un diccionario
    return {"message": "Hello World"}