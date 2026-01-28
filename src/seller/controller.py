from fastapi import APIRouter, HTTPException, Header

from typing import List

from .service import fetchSeller, registerSeller, fetchSellerListings, fetchSellerItems
from .model import SellerID, BecomeSeller, SellerListing, SellerItem
from ..auth.service import verifyJWT, createJWT, verifySeller

router= APIRouter(prefix="/seller",tags=['Seller'])

# ------------- sellers ------------- #
@router.get("/",response_model=SellerID)
def getSellerToken(auth: str = Header(None)):
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

@router.get("/listings",response_model=List[SellerListing])
def getSellerListings(auth: str = Header(None)):
    seller = verifySeller(auth)
    result =  fetchSellerListings(seller_id=seller) 
    return result

@router.get("/items",response_model=List[SellerItem])
def getSellerItems(auth: str = Header(None)):
    seller = verifySeller(auth)
    result =  fetchSellerItems(seller_id=seller) 
    return result  