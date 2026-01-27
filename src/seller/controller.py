from fastapi import APIRouter, HTTPException, Header

from .service import fetchSeller, registerSeller
from .model import SellerID, BecomeSeller
from ..auth.service import verifyJWT, createJWT

router= APIRouter(prefix="/seller",tags=['Seller'])

# ------------- sellers ------------- #
@router.get("/",response_model=SellerID)
def getSellerID(auth: str = Header(None)):
    user = verifyJWT(auth)
    result = fetchSeller(user['sub'])
    if result:
        seller_token = createJWT(user_id = user['sub'], seller_id = result)
        return SellerID(seller_token = seller_token)
    else:
        raise HTTPException(404, "User isn't a registered seller")
    
@router.post("/",response_model=SellerID)
def addSeller(seller_data:BecomeSeller, auth: str = Header(None)):
    user = verifyJWT(auth)
    result = registerSeller(user['sub'], seller_data.name)
    seller_token = createJWT(user_id = user['sub'], seller_id = result)   
    return SellerID(seller_token = seller_token)     