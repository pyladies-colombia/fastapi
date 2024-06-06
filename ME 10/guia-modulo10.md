# Módulo 10

## Creador: Esteban Maya Cadavid


# ¿Qué son los tipos de datos?

En Python, un **tipo de dato** define el tipo de valor que una variable puede almacenar. Esto ayuda a Python a saber qué operaciones se pueden realizar con los datos y a prevenir errores.

# Tipos de datos básicos en Python

### 1. Números

- **Enteros (`int`)**: Números enteros sin parte decimal.
  ```python
  edad = 25
  ```
- **Flotantes (`float`)**: Números con parte decimal.
  ```python
  precio = 19.99
  ```

### 2. Cadenas de texto (`str`)
Las cadenas de texto son secuencias de caracteres.

  ```python
  nombre = "Juan"
  ```

### 3. Booleanos (`bool`)
Los booleanos representan valores de verdad: `True` o `False`.
  ```python
  es_mayor = True
  ```

### 4. Listas (`list`)
Las listas son colecciones ordenadas y mutables de elementos.
  ```python
  frutas = ["manzana", "banana", "cereza"]
  ```

### 5. Tuplas (`tuple`)
Las tuplas son colecciones ordenadas e inmutables de elementos.
  ```python
  coordenadas = (40.7128, -74.0060)
  ```

### 6. Conjuntos (`set`)
Los conjuntos son colecciones desordenadas de elementos únicos.
  ```python
  colores = {"rojo", "verde", "azul"}
  ```

### 7. Diccionarios (`dict`)
Los diccionarios son colecciones de pares clave-valor.
  ```python
  persona = {
    "nombre": "Ana",
    "edad": 30,
    "ciudad": "Madrid"
}
  ```

## Cómo verificar el tipo de una variable
Puedes usar la función `type()` incluida en `python` para verificar el tipo de una variable.
  ```python
  numero = 42
  print(type(numero))  # Output: <class 'int'>
  ```

## Conversión de tipos (Type Casting)
A veces, necesitas convertir el tipo de una variable a otro tipo. Esto se llama **conversión de tipos** o **type casting.**
- De entero a cadena:
  ```python
  edad = 25
  edad_str = str(edad)
  ```
- De cadena a entero:
  ```python
  edad_str = "25"
  edad = int(edad_str)
  ```
- De flotante a entero:
  ```python
  precio = 19.99
  precio_entero = int(precio)  # Output: 19
  ```

# Tipos de datos avanzados en Python

## Tipos Genéricos

Los tipos genéricos permiten definir clases y funciones que pueden trabajar con cualquier tipo de dato. Esto es útil para crear estructuras de datos y algoritmos genéricos.

### Ejemplo 1: Lista Genérica

```python
from typing import List, TypeVar

T = TypeVar('T')

def invertir_lista(lista: List[T]) -> List[T]:
    return lista[::-1]

print(invertir_lista([1, 2, 3]))       # Output: [3, 2, 1]
print(invertir_lista(["a", "b", "c"])) # Output: ["c", "b", "a"]
```
#### Explicación
- TypeVar define un parámetro de tipo genérico T.
- invertir_lista toma una lista de cualquier tipo T y devuelve una lista del mismo tipo T

## `Union` y el Operador `|`
`Union` permite definir una variable que puede ser de más de un tipo. En **Python 3.10**, se introdujo el operador `|` como una forma más concisa de expresar esto.


### Ejemplo 2: Uso de `Union`

```python
from typing import Union

def procesar_datos(data: Union[int, str]) -> str:
    if isinstance(data, int):
        return f"Número procesado: {data}"
    elif isinstance(data, str):
        return f"Texto procesado: {data}"

print(procesar_datos(42))       # Output: Procesado número: 42
print(procesar_datos("hola"))   # Output: Procesado texto: hola
```

### Ejemplo 3: Uso del Operador `|`
```python
def procesar_datos_v2(data: int | str) -> str:
    if isinstance(data, int):
        return f"Número procesado: {data}"
    elif isinstance(data, str):
        return f"Texto procesado: {data}"

print(procesar_datos_v2(42))       # Output: Procesado número: 42
print(procesar_datos_v2("hola"))   # Output: Procesado texto: hola
```
#### Explicación
`Union[int, str]` y `int | str` indican que la variable data puede ser un entero o una cadena.

## `Annotated` para Metadatos.
`Annotated` permite agregar metadatos a los tipos, lo cual es útil para validación y documentación.

### Ejemplo 4: Uso de `Annotated` con Pydantic
```python
from typing import Annotated
from pydantic import BaseModel, Field

class Usuario(BaseModel):
    nombre: Annotated[str, Field(max_length=30)]
    edad: Annotated[int, Field(gt=0)]

usuario = Usuario(nombre="Juan", edad=25)
print(usuario)  # Output: nombre='Juan' edad=25
```
#### Explicación
`Annotated` permite agregar restricciones y descripciones a los campos, como `max_length` y `gt`.

## Tipos Literales
Los tipos literales permiten restringir una variable a un conjunto fijo de valores.

### Ejemplo 5: Uso de `Literal`
```python
from typing import Literal

def obtener_estado(estado: Literal["activo", "inactivo", "pendiente"]) -> str:
    if estado == "activo":
        return "El usuario está activo"
    elif estado == "inactivo":
        return "El usuario está inactivo"
    elif estado == "pendiente":
        return "El estado del usuario está pendiente"

print(obtener_estado("activo"))     # Output: El usuario está activo
print(obtener_estado("inactivo"))   # Output: El usuario está inactivo
print(obtener_estado("pendiente"))  # Output: El estado del usuario está pendiente
```
#### Explicación
`Literal` restringe el valor del parámetro estado a los valores específicos "activo", "inactivo" y "pendiente".


## Alias de Tipos
Los alias de tipos permiten crear nombres más significativos para tipos complejos.

### Ejemplo 6: Uso de `TypeAlias`
```python
from typing import TypeAlias

UsuarioID: TypeAlias = int

def obtener_usuario(usuario_id: UsuarioID) -> str:
    return f"Obteniendo usuario con ID: {usuario_id}"

print(obtener_usuario(101))  # Output: Obteniendo usuario con ID: 101
```
#### Explicación
`TypeAlias` define `UsuarioID` como un alias para `int`, lo que hace el código más legible y auto-documentado.

## Protocolos para Tipos Estructurales
Los protocolos permiten definir tipos que deben cumplir con una estructura específica, sin herencia explícita.

### Ejemplo 7: Uso de `Protocol`
```python
from typing import Protocol

class Describible(Protocol):
    def describir(self) -> str:
        ...

class Producto:
    def describir(self) -> str:
        return "Este es un producto"

class Servicio:
    def describir(self) -> str:
        return "Este es un servicio"

def imprimir_descripcion(item: Describible) -> None:
    print(item.describir())

producto = Producto()
servicio = Servicio()

imprimir_descripcion(producto)  # Output: Este es un producto
imprimir_descripcion(servicio)  # Output: Este es un servicio
```
#### Explicación
`Protocol` define una estructura que debe ser implementada por cualquier clase que use `Describible`.

### FastAPI y tipos
Puedes encontrar algunos ejemplos básicos de implementaciones de tipos en el script `fastapi_ejemplos.py`


### Conclusión
Entender los tipos de datos es fundamental para escribir programas efectivos en Python. Estos conceptos básicos te ayudarán a gestionar y manipular datos de manera eficiente, adicional te ayudaran a evitar cometer errores de tipos con ayuda de tu IDE favorito.

### Reto
#### Ya que has llegado al módulo extra de tipos, que tal si practicamos todo lo aprendido implementando los tipos que has visto en los módulos del 3 al 9, reescribe todos los ejemplos implementando las validaciones de tipos que más crees convenientes!
- Ejemplo: en el módulo 4, trata de agregar `Annotated` en todos los parámetros del servicio `/menu_items/{item_id}`, agregale solo un comentario para describir de que trata el parametro, asi puedes ver como funciona este tipo de anotación y como se refleja en `/docs`
- Ejemplo: En el módulo 5, implementar un Literal dentro de la clase `Reservation` de pydantic, para limitar el campo `name` solo pueda aceptar los nombres de `["pepe", "carlos", "juan"]`
- Continua implementando más tipos en todos los módulos restantes para que sigas practicando!
