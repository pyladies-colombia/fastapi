# Módulo 7: Ejemplo intermedio #2 - Autenticación y Autorización

### Creadora: Carolina Gómez

## Descripción

> Imagina que te acaban de compartir acceso a un documento de texto, pero cuando das clic en el
> enlace al documento te dice que **no tienes acceso** 🛑. ¿Cómo lo abririas?

En ese caso, podrías registrarte con tu cuenta de correo electrónico y luego podrás ver el contenido del documento.
En este proceso tuviste la oportunidad de usar los dos conceptos que veremos en esta guía, Autenticación y Autorización.

### ¿Qué es Autenticación?
La autenticación es el proceso mediante el cual se verifica la identidad de un usuario.

### ¿Qué es Autorización?
La autorización es el proceso mediante el cual se determina un usuario autenticado, a que recursos podrá acceder.

Para lograr esto en nuestras aplicaciones, podemos hacer uso de **OAuth2**, esta es una especificación que define diferentes maneras de manejar la Autorización y Autenticación de servicios.
Puedes leer más sobre ella [aquí](https://oauth.net/2/).

Vamos a ver un ejemplo para aplicar estos conceptos con **FastAPI**.

> Usaremos como base el ejemplo dado en el tutorial de FastAPI: [Security - First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

## Ejemplo

Imagina que tienes una aplicación en donde quieres agregar un sistema de autenticación para tus usuarios usando usuario y contraseña.

### Paso 1: Configuración del Entorno

Primero, asegúrate de tener Python 3.10 instalado. Luego, crea un entorno virtual e instala FastAPI.

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

# Instalar librerias
pip install fastapi
```
### Paso 2: Esqueleto de la aplicación
Dentro de tu ambiente virtual crea un archivo llamado `main.py` con la siguiente información:

```python
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}
```

Para correr el código anterior debes abrir una terminal y poner las siguientes instrucciones:

```bash
fastapi dev main.py
```
Para validar que todo esté funcionando bien, debes ir a la siguiente URL en tu navegador: [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/)
![](./images/image01.png)

Puedes ver un candado en la parte derecha del endpoint, si le das clic, podrás agregar información de autenticación como usuario y contraseña:
![](./images/image02.png)

Para entender un poco mejor el código anterior, vamos a ir paso a paso explicando cada línea, en esta oportunidad vamos a usar el 
flujo de contraseña. Gráficamente sería algo así:
![](./images/password-flow.png)

El usuario ingresa su nombre de usuario y contraseña y pulsa enter en la página web (cliente), luego esta información es enviada al servidor
que válida si este usuario existe, en ese caso responde con un token de acceso, este podrá ser usado para identificar la autorización del usuario.

En esta línea creamos una instancia de `OAuth2PasswordBearer`, dado que vamos a usar un token tipo Bearer:
```
...
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
...
```
Para usar dicho token en esta línea lo agregamos como una dependencia del endpoint:
```
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
```
**FastAPI** sabrá que puede usar esta dependencia para definir un esquema seguro en la documentación de la API.
Internamente, se valida que la petición tenga un encabezado llamado `Authorization` con el valor `Bearer <token>`.
Si este valor no es enviado se retorna un código de estado `HTTP 401 UNAUTHORIZED`. Si quieres saber más sobre 
los códigos de estado de HTTP puedes ver [este enlace](https://developer.mozilla.org/es/docs/Web/HTTP/Status).

### Paso 3: Envío de usuario y contraseña
OAuth2 especifica que el usuario y contraseña deben enviarse como `username` y `password` y de tipo `FormData`.
Si quieres conocer más sobre este tipo puedes leer la siguiente información: [Usando Objetos FormData](https://developer.mozilla.org/es/docs/Web/API/XMLHttpRequest_API/Using_FormData_Objects).
Esto lo podemos lograr en **FastAPI** utilizando una instancia de `OAuth2PasswordRequestForm`.

Vamos a sobreescribir el contenido del archivo `main.py` con la siguiente información:

```python
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# Usuarios de prueba
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```
En el archivo `main.py`, vamos a crear un modelo de Pydantic para el usuario:

```python

class User(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

```
Luego vamos a crear las siguientes funciones para obtener información del usuario:
```python
# hash de la contraseña
def fake_hash_password(password: str):
    return "fakehashed" + password
    
    
# Obtener usuario
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)

# Obtener token
def fake_decode_token(token):
    # Este código es de prueba, no usar en producción.
    user = get_user(fake_users_db, token)
    return user

# Obtener el usuario actual
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales Inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# Obtener los usuarios habilitados
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuario Inactivo")
    return current_user
```

Ahora vamos a crear el endpoint para hacer la autenticación de la aplicación:
```python
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecta")
    user = User(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrecta")

    return {"access_token": user.username, "token_type": "bearer"}
```

Esta función primero obtiene el `username` del usuario y válida que el usuario exista, en caso tal de que no
se lanza una excepción diciendo que el usuario es incorrecto.
Luego válida que la contraseña sea correcta, en caso de que no, también lanza una excepción.
Finalmente, si el usuario y contraseña existen, se retorna un token de acceso.

Ahora vamos a agregar el endpoint para ver la información del usuario que ha accedido a nuestra aplicación:
```python
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
```

Vamos a probar nuestro código, abre la siguiente URL [http://127.0.0.1:8000/docs]( http://127.0.0.1:8000/docs):
1. Clic en el botón de `Authorize`
2. Ingresa el usuario: `johndoe`
3. Ingresa la contraseña: `secret`
![](./images/image04.png)
4. Da clic en el botón `Authorize` y verás lo siguiente:
![](./images/image05.png)

Ahora puedes ir al endpoint `/users/me` y darle clic en la opción `Execute` y podrás ver la información de nuestro usuario de prueba:
![](./images/image06.png)

Si le das clic al icono del candado y luego al botón `Logout`, y ejecutas de nuevo la petición como indicamos anteriormente obtendrás el siguiente error:
```
{
  "detail": "Not authenticated"
}
```

Ahora intenta ingresar nuestro segundo usuario, autentícate con este usuario y luego llama al endpoint de `/users/me`:
```
Usuario: alice
Contraseña: secret2
```

¿Qué sucede?

### Paso 4: OAuth2 con contraseña (usando hashing) y Bearer con JWT
En la siguiente sección vamos a agregarle una capa de seguridad a nuestra aplicación, utilizando hash para que el almacenamiento 
de nuestras contraseñas sea más seguro y usando JWT (JSON Web Tokens).

#### ¿Qué son los JSON Web Tokens (JWT)?
Este es un estándar para codificar objetos JSON y que se puedan transmitir de una forma segura.
La información no está encriptada, o sea que cualquiera puede ver el contenido, pero si se encuentra firmada.
Esto quiere decir que si tú creas un token, podrías validar si este fue cambiado o si es un token válido.
Así luce un JWT:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```
Si quieres saber más sobre la estructura de un JWT, puedes ver el [siguiente link](https://jwt.io/introduction).

Para usar JWT en nuestra aplicación debemos instalar la libreria [**PyJWT**](https://pypi.org/project/PyJWT/), en tu ambiente virtual escribe lo siguiente:
```
pip install pyjwt
```

En nuestro ejemplo hemos manejado el hash de las contraseñas como unos caracteres adicionales que se pone al inicio de la contraseña, 
pero esta práctica no es segura, por lo que usaremos una libreria que nos permitirá que la contraseña original no sea mostrada,
en cambio, tendremos una nueva secuencia de caracteres generada por la libreria, lo que nos permitirá que si en una ambiente real
de producción alguien acceda a nuestra base de datos, no tenga la información sensible de los usuarios como contraseñas en texto plano.

La libreria que usaremos se llama [**PassLib**](https://pypi.org/project/passlib/), y el algoritmo para el hashing que se recomienda es Bcrypt. Puedes instalarla con el siguiente comando:
```
pip install "passlib[bcrypt]"
```
Para esta nueva versión de nuestro ejemplo puedes crear un nuevo archivo `main.py` y sobreescribir el anterior con otro nombre,
en el repositorio hemos nombrado el paso anterior como `main_basic.py`.

Primero vamos a crear una llave secreta aleatorea para firmar nuestros JWT, abre una terminal y pon el siguiente comando:
```
openssl rand -hex 32
```

Copia la secuencia de caracteres que se genera y pégala en la variable `SECRET_KEY` que crearemos a continuación:
```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
```

Como puedes observar en la variable `fake_users_db`, el campo `hashed_password`, tiene una version diferente de la contraseña del usuario.
Así es como lucen ahora nuestras contraseñas después de aplicarles el proceso de hashing.

Ahora vamos a crear un modelo de Pydantic para el token y unas funciones para acceder a dicho token:
```python

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


# Válida la contraseña
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Obtiene el hash de la contraseña
def get_password_hash(password):
    return pwd_context.hash(password)


# Obtiene el usuario
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

    
# Autentica el usuario
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Crea un token de acceso
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```
Ahora vamos a modificar nuestras funciones para obtener los usuarios y usaremos JWT:
```python
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pueden validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Usuario Inactivo")
    return current_user
```
Como puedes observar en la función `get_current_user`, se hace una descodificación del token del usuario y se válida 
que si exista. La llave `sub`del token es usada para poner la identificación del usuario, en este caso el `username`.

Nuestros endpoints también cambian un poco al usar JWT, en este caso el endpoint `/token` ahora genera un token que expira 
después de ciertos minutos, y tiene la información del usuario:
```python
@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o Contraseña Incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]
```
Ahora sí, es momento de validar nuestra aplicación, recuerda que para correrla debes ejecutar el comando:
```bash
fastapi dev main.py
```
Abre la siguiente URL [http://127.0.0.1:8000/docs]( http://127.0.0.1:8000/docs) y verás algo asi:
![](./images/image07.png)
1. Clic en el botón de `Authorize`
2. Ingresa el usuario: `johndoe`
3. Ingresa la contraseña: `secret`
![](./images/image08.png)

Ahora puedes ir al endpoint `/users/me` y darle clic en la opción `Execute` y podrás ver la información de nuestro usuario de prueba:
![](./images/image09.png)

Si abres el `developer tools`del navegador, haciendo clic derecho `Inspect` o Inspeccionar, y luego yendo a Network,
puedes ver que cada vez que le des clic a `Execute` se envía nuestro token de acceso:
![](./images/image10.png)

Una vez pasados los 30 minutos desde que generamos nuestro token, podrás ver que este ya no es válido y debes generar uno 
nuevo para consultar el endpoint `/users/me`.