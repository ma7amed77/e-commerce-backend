from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from .model import LoginData, RegisterData
from .service import authLogin, registerUser, createJWT

router= APIRouter(prefix="/auth",tags=['Auth'])

# ------------- users ------------- #
@router.post("/login")
def login(data:LoginData):
    token = authLogin(data.email, data.password)
    if token: return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "Email or password is wrong")

@router.post("/register")
def register(data:RegisterData):
    try: 
        id = registerUser(**data.model_dump())
        if id:
            token = createJWT(id)
            return {"access_token": token, "token_type": "bearer"} 
        else:
            raise HTTPException(status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Internal Error")
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Email already registered")