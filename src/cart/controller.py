from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import IntegrityError
from typing import List
from .service import fetchCart, addCartItem, deleteCartItem, updateCartItem
from .model import CartData, CartUpdate
from ..auth.service import verifyJWT
from ..schema import get_conn

router= APIRouter(prefix="/cart",tags=['Cart'])

# ------------- cart ------------- #
@router.get("/", response_model=List[CartData])
def getCart(conn:get_conn, auth: str = Header(None)):
    user = verifyJWT(auth)
    result = fetchCart(conn, user["sub"])
    return result

@router.post("/{listing_id}")
def addToCart(conn:get_conn, listing_id:int, auth: str = Header(None)):
    try:
        user = verifyJWT(auth)
        addCartItem(conn, listing_id, user['sub'])
        return {"message":"Item added"}
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_CONTENT, detail = "listing not found")
    
@router.delete("/{listing_id}")
def deleteFromCart(conn:get_conn, listing_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)
    result = deleteCartItem(conn, listing_id, user['sub'])
    if result: return {"message":"Item deleted"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found in cart")

@router.put("/{listing_id}")
def editCart(conn:get_conn, cartData:CartUpdate, listing_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)
    if cartData.amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount cannot be negative")
    result = updateCartItem(conn, listing_id, user['sub'], cartData.amount)
    if result: return {"message":"Item updated"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found in cart")
        