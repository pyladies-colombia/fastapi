# Módulo 6: Ejemplo Intermedio #1: - Gestión de Base de Datos con SQLModel ⛁

### Creadora: Alejandra

## Descripción

En este módulo aprenderemos a gestionar una base de datos en tu app de FastAPI con SQLModel. 

Antes de comenzar, es importante que tengas algunos conocimientos básicos.

### ¿Qué es SQLModel?

<a href="https://sqlmodel.tiangolo.com/" target="_blank">SQLModel</a> es una herramienta diseñada para interactuar con bases de datos SQL en apps de FastAPI, combinando <a href="https://www.sqlalchemy.org/" target="_blank">SQLAlchemy</a> y <a href="https://docs.pydantic.dev/latest/" target="_blank">Pydantic</a>. Es la ORM recomendada por FastAPI para trabajar con bases de datos SQL, aunque no es exclusiva de FastAPI y puede ser utilizada independientemente.

### ¿Qué es una ORM?

ORM (Object Relational Mapping), es una herramienta de programación que permite convertir datos entre sistemas incompatibles en objetos de programación, por ejemplo, entre una base de datos relacional y un lenguaje de programación, permite traducir de SQL a código Python y viceversa, todo usando clases y objetos.

## Ejemplo

Imagina que necesitas gestionar la base de datos de tu app de reservas:

### Paso 1: Instalar SQLModel

```bash
pip install sqlmodel
```

### Paso 2: Crear un modelo de SQLModel 

```python
from sqlmodel import Field, SQLModel
from datetime import datetime

class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None
```

La clase `Reservation` es un modelo de SQLModel, el equivalente a una tabla SQL en código Python y cada atributo de la clase es equivalente a una columna de la tabla.

### Paso 3: Crear el motor de la base de datos (engine)

Para crear el motor de la base de datos de SQLAlchemy, necesitas importar la función `create_engine` de SQLModel y pasarle la URL de la base de datos. 

Cada URL de base de datos tiene un formato específico, por ejemplo, para SQLite, (que es la base de datos que usaremos en este ejemplo), la URL es `sqlite:///` seguido del nombre del archivo de la base de datos, en este caso, `database.db`:


```python
from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

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


### Paso 4: Crear la base de datos y la tabla

Crear el motor de base de datos no crea el archivo de la base de datos, para crear la base de datos y la tabla, necesitas ejecutar `SQLModel.metadata.create_all(engine)`, esto creará el archivo `database.db` y la tabla `reservation` en la base de datos.


```python
from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime

class Reservation(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    datetime: datetime
    guests: int
    observation: str | None = None

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

SQLModel.metadata.create_all(engine)
```

### Paso 5: 


## Recursos adicionales

📝 **Introducción a bases de datos**: Consulta el capítulo de [`Intro to Databases`](https://sqlmodel.tiangolo.com/databases/) en la documentación oficial de SQLModel si quieres aprender más sobre bases de datos.

📝 **ORMs**: Consulta el capítulo de [`Database to Code (ORMs)`](https://sqlmodel.tiangolo.com/db-to-code/) en la documentación oficial de SQLModel si quieres profundizar más sobre ORMs.


📝 **Tutorial de SQLModel**: Consulta el capítulo de [`Tutorial - UserGuide`](https://sqlmodel.tiangolo.com/tutorial/) en la documentación oficial de SQLModel si quieres aprender más sobre SQLModel.
