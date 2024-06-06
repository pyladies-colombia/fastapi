import asyncio

from fastapi import FastAPI

app = FastAPI()


async def heat_water():
    print("Calentando agua...")
    await asyncio.sleep(2)  # Simula el tiempo para calentar agua
    print("Agua caliente lista.")
    return "agua caliente"


async def add_ingredients(ingredients):
    print(f"Añadiendo ingredientes: {ingredients}...")
    await asyncio.sleep(3)  # Simula el tiempo para mezclar y cocinar brevemente
    print(f"{ingredients} añadidos y cocinados.")
    return "sopa cocinada"


async def bake(time):
    print(f"Horneando durante {time} segundos...")
    await asyncio.sleep(time)  # Simula el tiempo de horneado
    print("Horneado completo.")
    return "plato horneado"


async def decorate(dessert):
    print(f"Decorando {dessert}...")
    await asyncio.sleep(1)  # Simula el tiempo de decoración
    print(f"{dessert} decorado.")
    return f"{dessert} listo"


async def prepare_soup():
    water = await heat_water()
    soup = await add_ingredients("vegetales y especias")
    return soup


async def prepare_main_course():
    main_course = await bake(5)  # Asume un horneado de 5 segundos
    return main_course


async def prepare_dessert():
    dessert = await bake(2)  # Asume un horneado de 2 segundos
    decorated_dessert = await decorate("pastel")
    return decorated_dessert


@app.get("/prepare_dinner")
async def prepare_dinner():
    soup_task = asyncio.create_task(prepare_soup())
    main_course_task = asyncio.create_task(prepare_main_course())
    dessert_task = asyncio.create_task(prepare_dessert())
    await asyncio.gather(soup_task, main_course_task, dessert_task)
    return {
        "message": "Cena completa",
        "soup": soup_task.result(),
        "main_course": main_course_task.result(),
        "dessert": dessert_task.result(),
    }
