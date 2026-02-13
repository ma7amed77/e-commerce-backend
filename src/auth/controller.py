from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .model import LoginData, RegisterData, Token
from .service import authLogin, registerUser, createJWT
from ..schema import get_conn

router= APIRouter(prefix="/auth",tags=['Auth'])

# ------------- users ------------- #
@router.post("/login", response_model=Token)
def login(conn:get_conn, data:LoginData):
    token = authLogin(conn, data.email, data.password)
    if token: return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Email or password is wrong")

@router.post("/register", response_model=Token)
def register(conn:get_conn, data:RegisterData):
    try: 
        id = registerUser(conn, **data.model_dump())
        if id:
            token = createJWT(id)
            return Token(access_token=token, token_type="bearer")
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Internal Error")
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email already registered")