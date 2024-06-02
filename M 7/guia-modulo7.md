# Módulo 7: Ejemplo intermedio #2 - Autenticación y Autorización

### Creadora: Carolina Gómez

## Descripción

> Imagina que te acaban de compartir acceso a un documento de texto, pero cuando das clic en el
> enlace al documento te dice que **no tienes acceso**. ¿Cómo lo abririas? 

En ese caso, podrías registrarte con tu cuenta de correo electrónico y luego podrás ver el contenido del documento.
En este proces tuviste la oportunidad de usar los dos conceptos que veremos en esta guía, Autenticación y Autorización.

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

Primero, asegúrate de tener Python 3.10 instalado. Luego, crea un entorno virtual e instala FastAPI, Uvicorn y Python Multipart (es necesario para enviar los datos).

```bash
# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows
venv\Scripts\activate
# En macOS/Linux
source venv/bin/activate

# Instalar FastAPI y Uvicorn
pip install fastapi uvicorn python-multipart
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
uvicorn main:app --reload
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
Si este valor no es enviado se retorna un código de estado `HTTP 401 UNAUTHORIZED`.

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

Ahora vamos a agregar el endpoint para ver los usuarios de nuestra aplicación:
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


