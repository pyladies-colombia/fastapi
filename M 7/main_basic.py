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


# Modelo de Pydantic
class User(BaseModel):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


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


# Endpoint para obtener el token de acceso
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


# Endpoint para obtener usuarios habilitados
@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
