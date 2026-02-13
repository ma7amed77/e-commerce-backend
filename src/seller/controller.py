from fastapi import APIRouter, HTTPException, Header

from typing import List

from .service import fetchSeller, registerSeller, fetchSellerListings, fetchSellerItems
from .model import SellerID, BecomeSeller, SellerListing, SellerItem
from ..auth.service import verifyJWT, createJWT, verifySeller
from ..schema import get_conn

router= APIRouter(prefix="/seller",tags=['Seller'])

# ------------- sellers ------------- #
@router.post("/",response_model=SellerID)
def getSellerToken(conn:get_conn, auth: str = Header(None)):
    user = verifyJWT(auth)
    result = fetchSeller(conn, user['sub'])
    if result:
        seller_token = createJWT(user_id = user['sub'], seller_id = result)
        return SellerID(access_token = seller_token)
    else:
        raise HTTPException(404, "User isn't a registered seller")
    
@router.post("/new",response_model=SellerID)
def addSeller(conn:get_conn, seller_data:BecomeSeller, auth: str = Header(None)):
    print(auth)
    user = verifyJWT(auth)
    result = registerSeller(conn, user['sub'], seller_data.name)
    seller_token = createJWT(user_id = user['sub'], seller_id = result)   
    return SellerID(access_token = seller_token)

@router.get("/listings",response_model=List[SellerListing])
def getSellerListings(conn:get_conn, auth: str = Header(None)):
    seller = verifySeller(auth)
    result =  fetchSellerListings(conn, seller_id=seller) 
    return result

@router.get("/items",response_model=List[SellerItem])
def getSellerItems(conn:get_conn, auth: str = Header(None)):
    seller = verifySeller(auth)
    result =  fetchSellerItems(conn, seller_id=seller) 
    return result  