from fastapi import FastAPI
import asyncio

app = FastAPI()

async def prepare_soup():
    print("Comenzando la sopa...")
    await asyncio.sleep(5)  # Simula 5 segundos de preparación
    print("Sopa lista.")

async def prepare_main_course():
    print("Comenzando el plato principal...")
    await asyncio.sleep(10)  # Simula 10 segundos de preparación
    print("Plato principal listo.")

async def prepare_dessert():
    print("Comenzando el postre...")
    await asyncio.sleep(3)  # Simula 3 segundos de preparación
    print("Postre listo.")

@app.get("/prepare_dinner")
async def prepare_dinner():
    asyncio.create_task(prepare_soup())  # Inicia la sopa y continúa
    asyncio.create_task(prepare_main_course())  # Inicia el plato principal y continúa
    asyncio.create_task(prepare_dessert())  # Inicia el postre y continúa
    return {"message": "La cena está siendo preparada..."}

