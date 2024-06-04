# Modulo 11: Dominando la programación asincróna en FastAPI

### Creadora: William Gómez

## Descripción
Este módulo proporciona una visión integral de cómo FastAPI maneja operaciones asíncronas y concurrentes para maximizar la eficiencia en aplicaciones web. 

## ¿Qué es la programación asincrona?
Imagina que estás preparando una cena que incluye tres platos: una sopa, un asado y un postre. Cada uno de estos platos requiere diferentes tiempos de preparación y cocción. En lugar de preparar cada plato de principio a fin de manera secuencia, comienzas calentando el agua para la sopa. Mientras el agua está calentándose, no te quedas mirando la olla; en lugar de eso, empiezas a preparar los ingredientes para el asado. Una vez que el agua empieza a hervir, añades los ingredientes de la sopa y bajas el fuego para que se cocine lentamente. No necesitas supervisar constantemente la sopa; puedes establecer un temporizador y comenzar a trabajar en el postre. Este enfoque te permite avanzar en la preparación del postre sin tener que esperar a que los otros platos estén completos. Al final, cada plato continúa cocinándose en su propio tiempo. Revisas y ajustas los platos según sea necesario, pero en general, estás libre para manejar otras tareas o descansar mientras todo se cocina.

## ¿En que se diferencia del paralelismo?
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

1. **Funciones Asíncronas**: Las funciones `prepare_soup`, `prepare_main_course`, y `prepare_dessert` son asíncronas. Usan `await asyncio.sleep()` para simular la espera durante la preparación de los alimentos. `asyncio.sleep()` es una función que pausa la función actual, liberando el bucle de eventos para que pueda hacer otras cosas, como atender otras solicitudes o continuar con otras tareas.

2. **Respuesta Inmediata**: El endpoint `/prepare_dinner` devuelve una respuesta inmediatamente después de iniciar las tareas. Informa al usuario que la cena está siendo preparada, pero no espera a que la preparación se complete. Esto podría ser útil en un contexto donde el usuario no necesita saber exactamente cuándo está todo listo, solo que el proceso ha comenzado.

3. **No sincronización de tareas**: Al no sincronizar las tareas, cada una se ejecuta de manera independiente. Esto podría reflejar un entorno real de cocina donde diferentes chefs trabajan en diferentes platos sin coordinarse para terminar al mismo tiempo.

### Paso 4: Ejecutar el Servidor

Ejecuta el servidor con Uvicorn utilizando el siguiente comando:

```bash
fastapi dev main.py
```

### Paso 5: Probar la API

Una vez que el servidor esté corriendo, puedes visitar `http://127.0.0.1:8000/prepare_dinner` en tu navegador o usar una herramienta como `curl` para hacer la solicitud y ver cómo se prepara la cena de manera asíncrona.