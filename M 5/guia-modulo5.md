# Módulo 5: Ejemplo básico #3 - Validación de datos con Pydantic 🕵🏻‍♀️

### Creadora: Alejandra

## Descripción

En este módulo aprenderemos a validar datos en FastAPI usando Pydantic.

### ¿Qué es Pydantic?

<a href="https://docs.pydantic.dev/latest/" target="_blank">Pydantic</a> es una herramienta que nos permite definir modelos de datos y validar los datos que recibimos en nuestra API.

### ¿Por qué es necesario validar datos en una API?

La validación de datos nos permite asegurarnos de que los datos que recibimos son los correctos y cumplen con ciertas reglas o restricciones. Por ejemplo, podemos validar que un campo sea de un cierto tipo, que cumpla con un formato específico, etc.

Sin validación, nuestra API podría recibir datos incorrectos, lo que podría llevar a errores en la aplicación.

## Ejemplo

**Nota:** Para este ejemplo, necesitas la versión 3.10 de Python. Puedes guiarte con el [Módulo 2](../M%202/guia-modulo2.md) para configurar tu entorno de desarrollo.

Imagina que tienes una API que recibe datos de un formulario en tu app para gestionar reservas en un restaurante. Para asegurarnos de que los datos que recibimos son los correctos, necesitamos validarlos.

Antes de comenzar, crea un archivo `main.py` y sigue los pasos a continuación.

### Paso 1: Importar BaseModel de Pydantic

Para usar Pydantic en nuestra API, primero debemos importar la clase `BaseModel` de Pydantic:

```python
from pydantic import BaseModel
```

### Paso 2: Definir un modelo de datos

El siguiente paso es definir un modelo de datos. Un modelo de datos es una clase que hereda de `BaseModel` y define los campos que esperamos recibir en nuestra API.

Por ejemplo, si nuestra API recibe datos de una reservación, podríamos definir un modelo de datos como el siguiente:

```python
# main.py

from pydantic import BaseModel
from datetime import datetime

class Reservation(BaseModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None 
```

### Paso 3: Añadir validaciones adicionales

Pydantic nos permite añadir validaciones adicionales a nuestros campos utilizando `Field`. Por ejemplo, podemos añadir una validación para asegurarnos de que el campo `guests` sea mayor que 0 y menor que 10. Primero, importamos `Field` de Pydantic. Luego, añadimos la validación al campo `guests` utilizando los argumentos `gt` y `lt` en `Field`, que representan "greater than" (mayor que) y "less than" (menor que), respectivamente.

```python
# main.py
from pydantic import BaseModel, Field
from datetime import datetime

class Reservation(BaseModel):
    name: str
    email: str
    datetime: datetime
    guests: int = Field(gt=0, lt=10)
    observation: str | None = None 
```

### Paso 4: Usar el modelo de datos en nuestra API

Para usar este modelo de datos en nuestra API, declaramos el tipo de nuestro argumento con el modelo que creamos:

```python
# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

class Reservation(BaseModel):
    name: str
    email: str
    datetime: datetime
    guests: int = Field(gt=0, lt=10)
    observation: str | None = None 

app = FastAPI()

@app.post("/reservation/")
async def create_reservation(reservation: Reservation):
    return reservation
```

### Paso 5: Ejecutar el servidor

Ejecuta el servidor con el siguiente comando:

```bash
fastapi dev main.py
```

### Paso 6: Probar con Swagger UI

Una vez que el servidor esté en funcionamiento, podemos probar nuestra API en Swagger UI. Si vamos a la URL `http://127.0.0.1:8000/docs`, veremos la documentación generada automáticamente por FastAPI con Swagger UI.

El modelo de datos creado se refleja en la documentación de Swagger, mostrando los campos esperados y sus tipos.

![](./images/image01.png)

Ahora podemos probar nuestra API enviando datos y ver cómo se validan automáticamente. Si probamos enviando datos válidos, nuestra API enviará una respuesta exitosa.

![](./images/image02.png)

Por el contrario, si enviamos un campo con algún dato que no cumpla con las reglas definidas en nuestro modelo de datos, Pydantic lanzará una excepción y FastAPI devolverá un error al cliente detalladamente.

![](./images/image03.png)

## Reto

💡 Ahora es tu turno, añade validaciones adicionales a los campos del modelo de datos `Reservation`, asegúrate que el campo `name` no esté vacío y que el campo `observation` tenga una longitud máxima de 100 caracteres.

Recuerda, la práctica hace al maestro. 🙇‍♀️ 
¡Buena suerte con tu reto! ✌️

## Recursos adicionales

📝 **Documentación de Pydantic**: Consulta la sección de [`String Constraints`](https://docs.pydantic.dev/latest/concepts/fields/#string-constraints) en la documentación oficial de Pydantic. Aquí encontrarás una descripción detallada de cómo puedes aplicar restricciones y validaciones a las cadenas de texto en tus modelos de datos.

📝 **Tutorial de FastAPI**: El [`Tutorial - User Guide`](https://fastapi.tiangolo.com/tutorial/) es una excelente fuente de información. Este tutorial cubre una amplia gama de temas, incluyendo la validación de datos, y puede ayudarte a entender cómo implementar y mejorar tus validaciones en FastAPI.
