# Modulo 2 - Preparando de tu PC

### Creadora: Laura López y Valen Ariza

# Configuración de ambiente

Este tutorial te guiará a través de los pasos necesarios para preparar tu PC, cubriremos la instalación de Python 3.10, FastAPI y uvicorn. 

Para utilizar FastAPI debes contar con un entorno controlado, esto se refiere a que vas a crear un entorno para asegurar estabilidad y reproducibilidad de tu código.

## Paso 1: Instalar Python 3.10

1.⁠ ⁠**Descargar Python 3.10**:
- Ve a la página oficial de descargas de Python: [Python.org](https://www.python.org/downloads/)
- Descarga el instalador correspondiente a tu sistema operativo (Windows, macOS o Linux).

2.⁠ ⁠**Instalar Python 3.10**:
- Ejecuta el instalador que descargaste.
- Asegúrate de marcar la opción "Add Python to PATH" antes de continuar con la instalación.
- Sigue las instrucciones del instalador para completar la instalación.

## Paso 2: Instalar FastAPI y Uvicorn

1.⁠ ⁠**Crear un entorno virtual**:
- Abre una terminal.
- Usando cd navega al directorio donde deseas crear tu proyecto.
- Ejecuta los siguientes comandos:
⁠ ```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate
 ⁠```
2.⁠ ⁠**Instalar FastAPI y Uvicorn**:
- Con el entorno virtual activado, ejecuta:
⁠ ```bash
pip install fastapi uvicorn
```

# Creando mi primer ¡Hola mundo!

## Paso 1: Crear un archivo main.py

 Abre main.py en tu editor de texto favorito y añade el siguiente código:

```
 from fastapi import FastAPI

 app = FastAPI()

 @app.get("/")
 async def root():
    return {"message": "Hello World"}

```

Puedes ver la información en el [archivo](./main.py)

## Paso 2: Ejecutar la aplicación

Utiliza Uvicorn para ejecutar la aplicación. Abre una terminal y ejecuta:

```bash
  fastapi dev <ruta_del_archivo>
```
Esto iniciará el servidor y podrás ver la salida en la terminal

![](./images/execute_app.png)

## Paso 3: Accede a la aplicación

Abre tu navegador y ve a http://127.0.0.1:8000. Deberías ver un mensaje de respuesta en formato JSON que dice {"message": "Hola Mundo"}.

![](./images/result.png)

Además, FastAPI genera automáticamente documentación interactiva para tu API. Puedes acceder a ella en:

**Documentación Swagger UI:** http://127.0.0.1:8000/docs

Esta es una interfaz interactiva que se genera automáticamente para explorar y probar las endpoints de la API directamente desde tu navegador. Puedes personalizarla cambiando el título, la descripción y otros detalles de la documentación.

Permite ver todos los endpoints disponibles en la API, junto con sus métodos HTTP (GET, POST, PUT, DELETE, etc.), parámetros, y descripciones.

Actualmente, esta documentación pasó a ser OpenAPI, una especificación para describir y documentar APIs de manera detallada y estandarizada, todo este proceso de forma automática. OpenAPI se ha convertido en el estándar de facto para la descripción de APIs RESTful.

![](./images/docs.png)

**Documentación ReDoc:** http://127.0.0.1:8000/redoc

Al igual que la documentación Swagger UI, la documentación ReDoc se genera automáticamente en FastAPI y proporciona una manera interactiva para explorar y probar las endpoints de tu API.

Redoc es compatible con la especificación OpenAPI, lo que significa que puede interpretar y mostrar las especificaciones OpenAPI de tu API de manera clara y precisa.

![](./images/redocs.png)

¡Y eso es todo! Ahora tienes una aplicación básica de FastAPI que devuelve un mensaje "Hola Mundo". Puedes expandir esta aplicación añadiendo más rutas y funcionalidades siguiendo los demás modulos.

## Recomendaciones:
Puedes crear un script para futuros proyectos, y con esto automatizar el proceso de instalación de dependencias:

1. Instala las dependencias necesarias: 
  - En el script puedes crear un entorno virtual y activarlo.
  - Actualizar pip para asegurarse de tener la última versión.
  - Instalar las dependencias necesarias (fastapi y uvicorn) utilizando pip.

Crea un archivo .sh con lo siguiente:
```bash
#!/bin/bash

# Crear y activar un entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar FastAPI y Uvicorn
pip install fastapi uvicorn
```

Si quieres saber más puedes dirigirte a la documentación oficial de [FastAPI](https://fastapi.tiangolo.com/learn/)