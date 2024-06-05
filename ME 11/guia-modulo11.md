# Modulo 11: Dominando la programación asíncrona en FastAPI

### Creadora: William Gómez

## Descripción
Este módulo proporciona una visión integral de cómo FastAPI maneja operaciones asíncronas y concurrentes para maximizar la eficiencia en aplicaciones web. 

## ¿Qué es la programación asíncrona?
Imagina que estás preparando una cena que incluye tres platos: una sopa, un asado y un postre. Cada uno de estos platos requiere diferentes tiempos de preparación y cocción. En lugar de preparar cada plato de principio a fin de manera secuencia, comienzas calentando el agua para la sopa. Mientras el agua está calentándose, no te quedas mirando la olla; en lugar de eso, empiezas a preparar los ingredientes para el asado. Una vez que el agua empieza a hervir, añades los ingredientes de la sopa y bajas el fuego para que se cocine lentamente. No necesitas supervisar constantemente la sopa; puedes establecer un temporizador y comenzar a trabajar en el postre. Este enfoque te permite avanzar en la preparación del postre sin tener que esperar a que los otros platos estén completos. Al final, cada plato continúa cocinándose en su propio tiempo. Revisas y ajustas los platos según sea necesario, pero en general, estás libre para manejar otras tareas o descansar mientras todo se cocina.

## ¿En qué se diferencia del paralelismo?
En el ejemplo de preparar una cena, aunque se está trabajando en varios platos al mismo tiempo, en realidad es un caso de asincronía y no de paralelismo. Aquí está el porqué:
1. Uso único de recursos:
En la cocina, aunque estás gestionando múltiples tareas (sopa, asado, postre), generalmente sólo estás realizando una acción a la vez. Por ejemplo, podrías estar picando verduras mientras el asado está en el horno, pero el acto físico de picar y supervisar el horno no ocurre exactamente al mismo tiempo. Estás alternando rápidamente tu atención y acciones entre tareas que esperan completarse
2. Limitación de procesadores (Humanos):
A diferencia del paralelismo real, donde múltiples procesadores o hilos pueden ejecutar tareas realmente en paralelo (simultáneamente), en este escenario de cocina, tú eres el único "procesador". Aunque puedes cambiar de una tarea a otra, no puedes físicamente realizar dos acciones exactamente al mismo tiempo. Claro que si invitas a varios de tus amigos a ayudarte con la cena, ahora si podríamos estar hablando de paralelismo.
3. Interdependencia de Tareas:
En la cocina, las tareas a menudo están interrelacionadas y requieren que se completen en cierto orden o que se gestionen secuencialmente (aunque de manera asincrónica). Por ejemplo, no puedes servir la sopa hasta que esté completamente cocida, y no puedes cocinar el postre sin haber preparado primero los ingredientes.

## ¿Es la concurrencia mejor que el paralelismo?
La concurrencia es diferente del paralelismo. Y es mejor en escenarios específicos que involucran mucha espera. Por eso, generalmente es mucho mejor que el paralelismo para el desarrollo de aplicaciones web. Pero no para todo.

Para equilibrar eso, imagina la siguiente historia corta:

Tienes que limpiar una casa grande y sucia.

Sí, esa es toda la historia.

En el contexto de limpiar una casa grande, el paralelismo sería muy beneficioso. Si una persona intenta hacer todo el trabajo por sí sola, tomaría mucho tiempo completarlo, porque las tareas (limpiar diferentes áreas) son independientes y pueden realizarse simultáneamente. Por lo tanto, tener múltiples personas (procesadores) trabajando en diferentes partes de la casa al mismo tiempo (paralelismo) sería más eficiente que una persona trabajando sola (concurrencia en un entorno limitado).

## Aplicación en Programación:
En un contexto de programación, esto es similar a iniciar una operación de entrada/salida (como leer un archivo o hacer una solicitud de red) y no bloquear el resto del programa mientras esperas que se complete. En lugar de eso, el programa puede continuar ejecutando otras tareas y luego manejar los resultados de la operación de I/O una vez que estén listos. Esta es la esencia de la programación asíncrona, donde se optimiza el tiempo y los recursos al no esperar de manera inactiva, permitiendo que múltiples procesos o tareas avancen en paralelo sin bloquearse entre sí.

## Ejemplo:
Este ejemplo simula una situación donde una API coordina diferentes tareas de preparación de una cena, cada una con tiempos de espera que imitan el tiempo de cocción o preparación.

### Paso 1: Instalación de FastAPI y Uvicorn

Primero, asegúrate de tener instalado FastAPI y Uvicorn, un servidor ASGI. Puedes instalarlos con pip:

```bash
pip install fastapi
```

### Paso 2: Crear el Archivo Principal de FastAPI

Crea un archivo `main.py`. Este archivo contendrá toda la lógica para manejar las diferentes tareas de la cena.

```python
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
```

### Paso 3: Explicación del Código

1. **Funciones Asíncronas**: Al definir una función con `async def`, estás creando una corutina. Una corutina es un tipo especial de función que puede pausar su ejecución antes de completar y esperar a que se complete otra operación asíncrona, sin bloquear el hilo de ejecución principal. Esto permite que otras corutinas se ejecuten en el mismo hilo mientras esta espera.

Dentro de una corutina, puedes usar `await` para suspender temporalmente la ejecución de la corutina hasta que se complete otra operación asíncrona. `await` solo puede ser usado dentro de una función definida con `async`.

Las funciones `prepare_soup`, `prepare_main_course`, y `prepare_dessert` son asíncronas. Usan `await asyncio.sleep()` para simular la espera durante la preparación de los alimentos. `asyncio.sleep()` es una función que pausa la función actual, liberando el bucle de eventos para que pueda hacer otras cosas, como atender otras solicitudes o continuar con otras tareas.

2. **Respuesta Inmediata**: El endpoint `/prepare_dinner` devuelve una respuesta inmediatamente después de iniciar las tareas. Informa al usuario que la cena está siendo preparada, pero no espera a que la preparación se complete. Esto podría ser útil en un contexto donde el usuario no necesita saber exactamente cuándo está todo listo, solo que el proceso ha comenzado.

3. **No sincronización de tareas**: Al no sincronizar las tareas, cada una se ejecuta de manera independiente. Esto podría reflejar un entorno real de cocina donde diferentes chefs trabajan en diferentes platos sin coordinarse para terminar al mismo tiempo.

### Paso 4: Ejecutar el Servidor

Ejecuta el servidor con Uvicorn utilizando el siguiente comando:

```bash
fastapi dev main.py
```

### Paso 5: Probar la API

Una vez que el servidor esté corriendo, puedes visitar `http://127.0.0.1:8000/prepare_dinner` en tu navegador o usar una herramienta como `curl` para hacer la solicitud y ver cómo se prepara la cena de manera asíncrona.

### Paso 6: Mejoremos nuestro código

Al visitar `http://127.0.0.1:8000/prepare_dinner` puedes notar que todas las tareas se ejecutan de manera concurrent pero el endpoint no esperaba explícitamente a que todas las tareas se completaran antes de enviar una respuesta. Esto significaba que la respuesta se enviaba inmediatamente después de iniciar las tareas, y la finalización de estas tareas no afectaba el momento de la respuesta del endpoint. 

Si modificamos un poco nuestro ejemplo y agregamos `asyncio.gather` luego de crear las tareas el comportamiento cambia:

```python
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
    soup_task = asyncio.create_task(prepare_soup())
    main_course_task = asyncio.create_task(prepare_main_course())
    dessert_task = asyncio.create_task(prepare_dessert())
    await asyncio.gather(soup_task, main_course_task, dessert_task)
    return {"message": "Cena completa"}
```

Con `asyncio.gather()`, el endpoint prepare_dinner ahora espera explícitamente que todas las tareas de preparación de los platos (sopa, plato principal, postre) se completen antes de enviar una respuesta. Esto asegura que la respuesta final del endpoint incluya los resultados de todas las tareas.

Con `asyncio.gather()`, no solo espera a que todas las tareas finalicen, sino que también maneja estas tareas de manera concurrente. Esto significa que las tareas se ejecutan en paralelo en el sentido de la concurrencia de asyncio, utilizando un único hilo pero alternando entre tareas durante las operaciones de espera.

### Paso 7: Un ejemplo un poco más elaborado

Vamos a expandir el ejemplo para que cada plato requiera de varios pasos en su preparación, utilizando más la sintaxis de `async` y `await`. Esto permitirá ilustrar cómo las tareas complejas pueden ser divididas en sub-tareas más pequeñas y manejadas de forma asíncrona en FastAPI.

```python
from fastapi import FastAPI
import asyncio

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
    return {"message": "Cena completa", "soup": soup_task.result(), "main_course": main_course_task.result(), "dessert": dessert_task.result()}
```