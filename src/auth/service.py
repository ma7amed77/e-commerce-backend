from fastapi import HTTPException
from sqlalchemy import select
from dotenv import load_dotenv


import jwt
import time
import os

from ..schema import users, engine
load_dotenv()
secret = os.getenv("SECRETKEY")
alg = "HS256"


# ------------ Users ------------- #
def fetchUserLogin(email:str):
    statement = select(users.c.name, users.c.user_id, users.c.password).where(users.c.email==email)
    with engine.connect() as conn:
        result = conn.execute(statement).fetchone()
        if result: return result._mapping
    return None

def registerUser(**kwargs):
    statement = users.insert().values(**kwargs)
    with engine.begin() as conn:
        result = conn.execute(statement)
        if result.inserted_primary_key:
            return result.inserted_primary_key[0]

def createJWT(user_id:int, seller_id: int | None = None):
    payload={
        "sub":str(user_id),
        "iat":int(time.time()),
        "exp":int(time.time())+3600,
        "seller_id":seller_id
    }
    token = jwt.encode(payload,secret, algorithm=alg)
    return token

def verifyJWT(token:str):
    try:
        payload = jwt.decode(token, secret, alg)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code = 401) 
    except jwt.InvalidTokenError:
        raise HTTPException(status_code = 401)

def authLogin(email:str,password:str):
    userData = fetchUserLogin(email)
    if not userData:
        return None
    if userData.password != password:
        return None
    return createJWT(userData.user_id)

def verifySeller(auth:str):
    user = verifyJWT(auth)
    seller_id = user['seller_id']
    if not seller_id : 
        raise HTTPException(status_code=403, detail="User is not a registered seller")
    return seller_id