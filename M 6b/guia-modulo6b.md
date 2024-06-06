# Módulo 6b: Ejemplo Intermedio #2: - *Dependencies* de FastAPI para acceder a un Speakeasy

### Creadora: Nathaly

## Descripción

En este módulo aprenderemos sobre las *dependencies* (dependencias) de FastAPI, y las usaremos para validar un token que permita el acceso. Al hacerlo con dependencies podemos gestionar la lógica compartida y modularizar nuestro código. Exploraremos un ejemplo práctico donde implementamos un menú de un restaurante secreto (speakeasy) que requiere una clave de acceso para poder ver los elementos del menú.

## Ejemplo

Antes de comenzar, asegúrate de tener tu entorno de desarrollo configurado. Te puedes guiar con el [Módulo 2](../M%202/guia-modulo2.md).

### Paso 1: Definición de los Elementos del Menú

En un archivo `main.py`, crea una aplicación FastAPI con una lista de diccionarios `menu_items`, donde cada diccionario representa un elemento del menú con su `item_id`, `name`, `description`, y `price`.

```python
menu_items = [
  {
    "item_id": 1,
    "name": "Bandeja Paisa",
    "description": "Traditional dish with beans, rice, pork, plantain, avocado, arepa, and egg",
    "price": 15.0
  },
  {
    "item_id": 2,
    "name": "Ajiaco",
    "description": "A hearty soup made from three different kinds of potatoes (criolla, sabanera and pastusa), chicken, guasca leaves, with a half an ear of corn splashed in for good measure",
    "price": 10.0
  },
  {
    "item_id": 3,
    "name": "Calentao",
    "description": "dish made from reheated leftovers including rice, egg, pasta, beans, potatoes and other foods such as arepa, chorizo, and ground beef",
    "price": 9.5
  },
  # ... otros elementos ...
]
```

### Paso 2: Función para Validar el Token

`get_token` es una función que valida la clave de acceso proporcionada en un parametro de consulta llamado `token` y, si es incorrecto, lanza una excepción HTTP 401.

```python
def get_token(token: str):
  if token != "girlsjustwannahavepython":
    raise HTTPException(status_code=401, detail="Solo las PyLadies pueden entrar")
  return token
```

Queremos que FastAPI ejecute esta función automaticamente antes de ejecutar los endpoints que requieran validación de acceso.
Para lograrlo, vamos a utilizar esta función como una dependencia de FastAPI.
`get_token` tiene un parámetro `token` de tipo `str`, cuando FastAPI ejecute esta función como una dependencia, automáticamente va a extraer el valor del parámetro de consulta (query) `token`.
Es decir, si alguien va a la URL:
```
https://pyladies-restaurant.example.com/menu_items/?token=girlsjustwannahavepython
```
FastAPI va a extraer el valor `girlsjustwannahavepython` y lo va a pasar como argumento a la función `get_token`.
También va a aparecer en la documentación automática con Swagger UI.
Una función de dependencia puede tener los mismos parámetros que una función de un endpoint, y así puede extraer datos de los parámetros de consulta (query), del cuerpo del mensaje, etc.

### Paso 3: Endpoint para Listar los Elementos del Menú

Para utilizar la función `get_token` como una dependencia de FastAPI, declaramos un nuevo parametro `token` en la función del endpoint. En vez de declarar el tipo como `str`, utilizamos `Annotated` y dentro de `Annotated` ponemos el tipo `str` y usamos `Depends(get_token)`.
Con `Depends(get_token)` le decimos a FastAPI que la función `get_token` es una dependencia.

```python
@app.get("/menu_items/")
def read_menu_items(token: Annotated[str, Depends(get_token)]):
  return menu_items
```

FastAPI va a ejecutar la función `get_token`, extraer los datos necesarios del mensaje (request), y va a pasar el resultado al parámetro que declaramos, en este caso también llamado `token`.

Así, solo quienes tengan el `token` secreto de `girlsjustwannahavepython` podrán ver el menú del restaurante.

### Paso 4: Endpoint para Leer un Elemento del Menú por ID

Este endpoint busca un elemento del menú por `item_id` y lo devuelve solo si el token es válido. Si no lo encuentra, lanza una excepción `HTTP 404`.

```python
@app.get("/menu_items/{item_id}", response_model=dict)
def read_menu_item(item_id: int, token: str = Depends(get_token)):
  for item in menu_items:
    if item["item_id"] == item_id:
      return item

  raise HTTPException(status_code=404, detail="No se encontró el ítem especificado")
```

### Paso 5: Probar la API desde Swagger UI

1. Abre tu navegador web y ve a http://127.0.0.1:8000/docs.

2. Usa los botones `Try it out` en cada endpoint para interactuar con la API:

    - GET `/menu_items/` para listar los elementos del menú.
    - GET `/menu_items/{item_id}` para obtener un elemento específico del menú por `item_id`.

*Nota:* Recuerda ingresar la clave de acceso para poder ver el menú del Speakeasy.

## Nuevo Reto

Agrega un endpoint para eliminar un ítem del menú, este se vería así:
    - DELETE `/menu_items/{item_id}` para eliminar un elemento del menú especificado por `item_id`.
