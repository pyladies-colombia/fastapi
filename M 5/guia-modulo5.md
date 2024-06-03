# Módulo 5: Validación de datos con Pydantic

### Creadora: Alejandra 

## Descripción

En este módulo aprenderemos a validar datos en FastAPI usando Pydantic.

### ¿Qué es Pydantic?

<a href="https://docs.pydantic.dev/latest/" class="external-link" target="_blank">Pydantic</a> es una librería que nos permite definir modelos de datos y validar los datos que recibimos en nuestra API.

### ¿Por qué es necesario validar datos?

La validación de datos es crucial para garantizar la integridad y seguridad de los datos, prevenir errores inesperados y mejorar la experiencia del desarrollador. Sin validación, nuestra API podría recibir datos incorrectos o maliciosos, lo que podría llevar a errores en la aplicación o a vulnerabilidades de seguridad.

## Ejemplo 

Imagina que tienes una API que recibe datos de un formulario. Para asegurarnos de que los datos que recibimos son los correctos, necesitamos validarlos.

### Paso 1: Importar BaseModel de Pydantic

Para usar Pydantic en nuestra API, primero debemos importar la clase `BaseModel` de Pydantic:

```python
from pydantic import BaseModel
```

### Paso 2: Definir un modelo de datos

El siguiente paso es definir un modelo de datos. Un modelo de datos es una clase que hereda de `BaseModel` y define los campos que esperamos recibir en nuestra API.

Por ejemplo, si nuestra API recibe datos de una reservación, podríamos definir un modelo de datos como el siguiente:

```python
class Reservation(BaseModel):
    name: str
    email: str
    date: date
    number_of_people: int
    price: float
    observation: str | None = None 
```

Para usar este modelo de datos en nuestra API, simplemente lo pasamos como argumento a nuestra función:

```python
@app.post("/reservation/")
async def create_reservation(reservation: Reservation):
    return reservation
```

