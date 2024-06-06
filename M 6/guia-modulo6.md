# Módulo 6: Ejemplo Intermedio #1: - Gestión de Base de Datos con SQLModel 🗃️

### Creadora: Alejandra

## Descripción

En este módulo aprenderemos a gestionar una base de datos en tu app de FastAPI con SQLModel.

Antes de comenzar, es importante que tengas algunos conocimientos básicos.

### ¿Qué es SQLModel?

<a href="https://sqlmodel.tiangolo.com/" target="_blank">SQLModel</a> es una herramienta diseñada para interactuar con bases de datos SQL en apps de FastAPI, combinando <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy</a> y <a href="https://docs.pydantic.dev/latest/" target="_blank">Pydantic</a>. Es el ORM recomendado por FastAPI para trabajar con bases de datos SQL, aunque no es exclusiva de FastAPI y puede ser utilizada independientemente.

### ¿Qué es un ORM?

Un ORM (Object Relational Mapper), es una herramienta de programación que permite convertir datos entre una base de datos relacional y un lenguaje de programación, permite traducir de SQL a código Python y viceversa, todo usando clases y objetos.

## Ejemplo

**Nota:** Para este ejemplo, necesitas la versión 3.10 o superior de Python. Puedes guiarte con el [Módulo 2](../M%202/guia-modulo2.md) para configurar tu entorno de desarrollo.

Imagina que necesitas gestionar la base de datos de tu app de reservas.

### Paso 1: Instalar SQLModel

```bash
pip install sqlmodel
```

### Paso 2: Crear un modelo de SQLModel 

En un archivo `main.py` crea un modelo de SQLModel para la tabla `reservation`:

```python
# main.py

from datetime import datetime

from sqlmodel import Field, SQLModel


class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None
```

La clase `Reservation` es un modelo de SQLModel, el equivalente a una tabla SQL en código Python, y cada atributo de la clase es equivalente a una columna de la tabla.

### Paso 3: Crear el motor de la base de datos (`engine`)

Para crear el motor de la base de datos, necesitas importar la función `create_engine` de SQLModel y pasarle la URL de la base de datos.

Cada URL de base de datos tiene un formato específico, por ejemplo, para SQLite, (que es la base de datos que usaremos en este ejemplo), la URL es `sqlite:///` seguido del nombre del archivo de la base de datos, en este caso, `database.db`:

```python
# main.py

from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine


class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
```

En este ejemplo, estamos usando el argumento `echo=True` para que el motor de la base de datos imprima todas las consultas SQL que se ejecutan en la consola, es particularmente útil para depurar y entender lo que está pasando en la base de datos.

**Nota:** El motor de la base de datos (`engine`) es un objeto que se encarga de la comunicación con la base de datos y de manejar las conexiones, se crea una sola vez y se reutiliza en toda la app.

### Paso 4: Crear la base de datos y la tabla

Crear el motor de base de datos no crea el archivo de la base de datos, para crear la base de datos y la tabla, necesitas ejecutar `SQLModel.metadata.create_all(engine)`, esto creará el archivo `database.db` y la tabla `reservation` en la base de datos.

```python
# main.py

from datetime import datetime

from sqlmodel import Field, SQLModel, create_engine


class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
```

### Paso 5: Correr el programa

Para correr el programa, ejecuta el siguiente comando:

```bash
python main.py
```

Si todo está correcto, verás lo siguiente en la consola:

```
2024-06-04 22:52:56,487 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine PRAGMA main.table_info("reservation")
2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine PRAGMA temp.table_info("reservation")
2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine [raw sql] ()
2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine 
CREATE TABLE reservation (
        id INTEGER NOT NULL, 
        name VARCHAR NOT NULL, 
        email VARCHAR NOT NULL, 
        datetime DATETIME NOT NULL, 
        guests INTEGER NOT NULL, 
        observation VARCHAR, 
        PRIMARY KEY (id)
)


2024-06-04 22:52:56,488 INFO sqlalchemy.engine.Engine [no key 0.00008s] ()
2024-06-04 22:52:56,513 INFO sqlalchemy.engine.Engine COMMIT

```

Esto significa que la tabla `reservation` fue creada con éxito en la base de datos `database.db` y se verá algo así (aunque por el momento aún no hay registros):

| id       | name    | email             | datetime            | guests | observation   |
| -------- | ------- | ----------------- | ------------------- | -------| ------------- |
| 1        | Ana     |ana@domain.com     | 2024-06-04 22:52:56 | 2      | None          |
| 2        | Jane    |jane@domain.com    | 2024-06-04 22:52:56 | 3      | Outside table |
| 3        | John    |john@domain.com    | 2024-06-04 22:52:56 | 6      | None          |

### Paso 6: Crear un modelo adicional

Como cada modelo de SQLModel es equivalente a un modelo de Pydantic, se puede usar para crear un endpoint en FastAPI. Sin embargo, si usamos el modelo que creamos anterioremente, se le estaría permitiendo al usuario escoger el `id` de la reserva en la base de datos, pero queremos que sea la base de datos la que decida el `id` en lugar del usuario. Para evitar esto, podemos crear un modelo adicional que no incluya el `id` al que llamaremos `ReservationBase`:

```python
# main.py

from datetime import datetime

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine


class ReservationBase(SQLModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None


class Reservation(ReservationBase, table=True):
    id: int = Field(default=None, primary_key=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
```

### Paso 7: Crear un endpoint en FastAPI

Primero crea un app de FastAPI y luego agrega un endpoint para crear una reserva:

```python
# main.py

from datetime import datetime

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine


class ReservationBase(SQLModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None


class Reservation(ReservationBase, table=True):
    id: int = Field(default=None, primary_key=True)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/reservations/")
def create_reservation(reservation: ReservationBase):
    return reservation
```

Ahora que tenemos el modelo de `ReservationBase` lo podemos usar en el nuevo endpoint `create_reservation` que creamos en FastAPI.

**Nota:** Hasta este paso el endpoint `create_reservation` solo retorna la reserva que recibe para probar que todo está funcionando correctamente.

### Paso 8: Guardar la reserva

Lo primero que necesitamos es importar `Session` de SQLModel y luego crear una sesión con el motor de la base de datos (`engine`), en nuestro ejemplo lo haremos en el mismo endpoint.

**Nota:** La sesión (`session`) usa el motor de la base de datos (`engine`) para comunicarse con la base de datos y se usa una por request.

En un bloque `with`, creamos una sesión, pasando `engine` como parámetro. 

Luego utilizamos el método de `model_validate()` para crear un objeto de tipo `Reservation` a partir del objeto de tipo `ReservationBase` que recibimos en el endpoint.

Luego con los métodos `add()`, `commit()` y `refresh()` de la sesión agregamos, guardamos y refrescamos la reserva en la base de datos y finalmente la retornamos.

La sesión se cerrará automáticamente al final del bloque `with`.


```python
# main.py

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime

class ReservationBase(SQLModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None

class Reservation(ReservationBase, table=True):
    id: int = Field(default=None, primary_key=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/reservations/")
def create_reservation(reservation: ReservationBase):
    with Session(engine) as session:
        db_reservation = Reservation.model_validate(reservation)
        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)
        return db_reservation
```

## Paso 9: Leer las reservas

Primero, importa `select` de SQLModel y luego crea un nuevo endpoint para leer las reservas. De igual manera que en el paso anterior, primero creamos una sesión y luego ejecutamos una consulta para obtener todas las reservas en la base de datos.

```python
# main.py

from fastapi import FastAPI
from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import datetime

class ReservationBase(SQLModel):
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None

class Reservation(ReservationBase, table=True):
    id: int = Field(default=None, primary_key=True)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.post("/reservations/")
def create_reservation(reservation: ReservationBase):
    with Session(engine) as session:
        db_reservation = Reservation.model_validate(reservation)
        session.add(db_reservation)
        session.commit()
        session.refresh(db_reservation)
        return db_reservation

@app.get("/reservations/")
def read_reservations():
    with Session(engine) as session:
        reservations = session.exec(select(Reservation)).all()
        return reservations
```

## Reto

💡 Ahora es tu turno, crea un endpoint para eliminar una reserva.

Recuerda, la práctica hace al maestro. 🙇‍♀️ ¡Buena suerte con tu reto! ✌️

## Recursos adicionales

**Nota:** Este es un ejemplo simple con todo el código en un mismo archivo para facilitar el aprendizaje. Puedes consultar más en las siguientes fuentes donde aprenderás cómo estructurar mejor tus aplicaciones con múltiples archivos, manejar sesiones con Dependencies, agregar tests y profundizar más sobre otros temas:

📝 **Introducción a bases de datos**: Consulta el capítulo de [`Intro to Databases`](https://sqlmodel.tiangolo.com/databases/) en la documentación oficial de SQLModel si quieres aprender más sobre bases de datos.

📝 **ORMs**: Consulta el capítulo de [`Database to Code (ORMs)`](https://sqlmodel.tiangolo.com/db-to-code/) en la documentación oficial de SQLModel si quieres profundizar más sobre ORMs.

📝 **Tutorial de SQLModel**: Consulta el capítulo de [`Tutorial - UserGuide`](https://sqlmodel.tiangolo.com/tutorial/) en la documentación oficial de SQLModel si quieres aprender más sobre SQLModel.



