# Ejemplo 1 Lista generica

from typing import List, TypeVar, Union, Literal, Annotated, TypeAlias, Protocol, Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

T = TypeVar('T')

app = FastAPI()

@app.post("/invertir/")
def invertir_lista(lista: List[T]) -> List[T]:
    return lista[::-1]
    # Para probar esto, envía una solicitud POST con una lista de enteros o cadenas.
    # Ejemplo de solicitud: POST /invertir/ con cuerpo: [1, 2, 3]


# Ejemplo 2 uso de Union y operador `|`
class DataModel(BaseModel):
    data: Union[int, str]

@app.post("/procesar/")
def procesar_datos(data_model: DataModel) -> Any:
    if isinstance(data_model.data, int):
        return {"message": f"Procesado número: {data_model.data}"}
    elif isinstance(data_model.data, str):
        return {"message": f"Procesado texto: {data_model.data}"}
    # Ejemplo de solicitud: POST /procesar/ con cuerpo: {"data": 42} o {"data": "hola"}


# Ejemplo 3: Uso del Operador |
class DataModelV2(BaseModel):
    data: int | str

@app.post("/procesar_v2/")
def procesar_datos_v2(data_model: DataModelV2) -> Any:
    if isinstance(data_model.data, int):
        return {"message": f"Procesado número: {data_model.data}"}
    elif isinstance(data_model.data, str):
        return {"message": f"Procesado texto: {data_model.data}"}
    # Ejemplo de solicitud: POST /procesar_v2/ con cuerpo: {"data": 42} o {"data": "hola"}


# Ejemplo 4: Uso de Annotated con Pydantic
class Usuario(BaseModel):
    nombre: Annotated[str, Field(max_length=30)]
    edad: Annotated[int, Field(gt=0)]

@app.post("/usuarios/")
def crear_usuario(usuario: Usuario):
    return usuario
    # Ejemplo de solicitud: POST /usuarios/ con cuerpo: {"nombre": "Juan", "edad": 25}


# Ejemplo 5: Uso de Literal
@app.get("/estado/")
def obtener_estado(estado: Literal["activo", "inactivo", "pendiente"]) -> Any:
    if estado == "activo":
        return {"message": "El usuario está activo"}
    elif estado == "inactivo":
        return {"message": "El usuario está inactivo"}
    elif estado == "pendiente":
        return {"message": "El estado del usuario está pendiente"}
    # Ejemplo de solicitud: GET /estado/?estado=activo


# Ejemplo 6: Uso de TypeAlias
UsuarioID: TypeAlias = int

@app.get("/usuario/{usuario_id}")
def obtener_usuario(usuario_id: UsuarioID) -> Any:
    return {"message": f"Obteniendo usuario con ID: {usuario_id}"}
    # Ejemplo de solicitud: GET /usuario/101


# Ejemplo 7: Uso de Protocol
class Describible(Protocol):
    def describir(self) -> str:
        ...

class Producto:
    def describir(self) -> str:
        return "Este es un producto"

class Servicio:
    def describir(self) -> str:
        return "Este es un servicio"

def imprimir_descripcion(item: Describible) -> str:
    return item.describir()

@app.get("/descripcion/")
def obtener_descripcion(tipo: str) -> Any:
    if tipo == "producto":
        return {"message": imprimir_descripcion(Producto())}
    elif tipo == "servicio":
        return {"message": imprimir_descripcion(Servicio())}
    else:
        return {"message": "Tipo de descripción no encontrado"}
    # Ejemplo de solicitud: GET /descripcion/?tipo=producto

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # abre tu navegador y ve a http://127.0.0.1:8000/docs para probar todos los ejemplos
