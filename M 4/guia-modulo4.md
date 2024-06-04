# Módulo 4 - Gestión de menús y uso de dependencias.

### Creadora: Nathaly Riaño

## Descripción

En este módulo aprenderemos sobre el uso de dependencias en FastAPI, una herramienta que nos permite gestionar la lógica compartida y modularizar nuestro código. Exploraremos un ejemplo práctico donde implementamos un menú de restaurante con varias operaciones CRUD (Crear, Leer, Actualizar, Eliminar).

## Importancia del Manejo de Dependencias

El manejo de dependencias en FastAPI es crucial para mantener el código modular, reutilizable y fácil de mantener. Al usar dependencias, se puede gestionar la lógica común de una manera más estructurada, facilitando la inyección de dependencias en diferentes puntos de la aplicación. Esto ayuda a:

- Reducir la Duplicación de Código: La lógica común, como la obtención de datos o la validación, puede ser definida una vez y reutilizada.
- Mejorar la Legibilidad: Al separar las preocupaciones, el código principal de los endpoints se mantiene limpio y enfocado en la lógica específica del endpoint.
- Facilitar el Testeo: Las dependencias pueden ser fácilmente mockeadas durante las pruebas, lo que simplifica la creación de tests unitarios y de integración.

## Ejemplo práctico

**Antes de iniciar** asegúrate de tener los requerimientos indicados en el [Módulo 2](../M%202/guia-modulo2.md).

### Paso 1: Crear la Estructura del Proyecto

Crea la siguiente estructura de directorios y archivos para el proyecto:

```bash
restaurant_menu/
└── main.py
```

### Paso 2: Importación de Módulos y Definición de la Aplicación

Primero, inicializamos nuestra aplicación FastAPI:

- `FastAPI` se utiliza para crear la aplicación web.
- `Depends` se usa para manejar dependencias en los endpoints.
- `HTTPException` permite manejar excepciones HTTP.
- `Query` se utiliza para definir parámetros de consulta.
- `Union` y `Annotated` se utilizan para la tipificación y documentación de los parámetros

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from typing import Union, List

app = FastAPI()
```

### Paso 3: Definición de los Elementos del Menú

`menu_items` es una lista de diccionarios, donde cada diccionario representa un elemento del menú con su `item_id`, `name`, `description`, y `price`.

```python
menu_items = [
  {
    "item_id": 1,
    "name": "Bandeja Paisa",
    "description": "Traditional dish with beans, rice, pork, plantain, avocado, arepa, and egg",
    "price": 15.0
  },
  # ... otros elementos ...
]
```

### Paso 4: Función para Obtener el Menú

`get_menu` es una función que devuelve los elementos del menú y puede limitar el número de elementos devueltos usando el parámetro `limit`.

```python
def get_menu(
  limit: Annotated[Union[int, None],
  Query(description="Limit the number of menu items returned")] = None
):
  if limit:
    return menu_items[:limit]

  return menu_items
]
```

### Paso 5: Endpoint para Listar los Elementos del Menú

Este endpoint utiliza la función `get_menu` como una dependencia para obtener y devolver los elementos del menú.

```python
@app.get("/menu_items/", response_model=list[dict])
def read_menu_items(menu=Depends(get_menu)):
  return menu
```

### Paso 6: Endpoint para Leer un Elemento del Menú por ID

Este endpoint busca un elemento del menú por `item_id`. Si no lo encuentra, lanza una excepción `HTTP 404`.

```python
@app.get("/menu_items/{item_id}", response_model=dict)
def read_menu_item(item_id: int):
  for item in menu_items:
    if item["item_id"] == item_id:
      return item

  raise HTTPException(status_code=404, detail="Item not found")
```
### Paso 7: Endpoint para Actualizar un Elemento del Menú

Este endpoint permite actualizar un elemento del menú especificado por `item_id`. Actualiza el `name`, `description`, y `price` del elemento.

```python
@app.put("/menu_items/{item_id}", response_model=dict)
def update_menu_item(
  item_id: int,
  name: str,
  description: str,
  price: float
):
  for item in menu_items:
    if item["item_id"] == item_id:
      item.update({
        "name": name,
        "description": description,
        "price": price
      })
      return item

  raise HTTPException(status_code=404, detail="Item not found")
```

### Paso 8: Probar la API desde Swagger

Para probar la API, sigue estos pasos:

1. Abre tu navegador web y ve a http://127.0.0.1:8000/docs.
2. Usa los botones `Try it out` en cada endpoint para interactuar con la API:
    - GET `/menu_items/` para listar los elementos del menú, con la opción de limitar el número de elementos devueltos usando el parámetro `limit`.
    - GET `/menu_items/{item_id}` para obtener un elemento específico del menú por `item_id`.
    - PUT `/menu_items/{item_id}` para actualizar un elemento del menú especificado por `item_id`, proporcionando el `name`, `description` y `price`.

## Nuevos Retos

1. Extrae las funciones para listar los elementos del menú, listar un elemento del menú y actualizar un elemento del menú. Pista: Observa cómo la función `get_menu` se está usando como una dependencia en el endpoint para listar los elementos del menú.
2. Agrega un endpoint para eliminar un item del menú, este se vería así:
    - DELETE `/menu_items/{item_id}` para eliminar un elemento del menú especificado por `item_id`.