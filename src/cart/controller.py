from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import IntegrityError

from .service import fetchCart, addCartItem, deleteCartItem, updateCartItem
from .model import CartData
from ..auth.service import verifyJWT

router= APIRouter(prefix="/cart",tags=['Cart'])

# ------------- cart ------------- #
@router.get("/")
def getCart(auth: str = Header(None)):
    user = verifyJWT(auth)
    result = fetchCart(user["sub"])
    if not result:
        raise HTTPException(404, "User doesn't have a cart")
    return result

@router.post("/{listing_id}")
def addToCart(listing_id:int, auth: str = Header(None)):
    try:
        user = verifyJWT(auth)
        addCartItem(listing_id, user['sub'])
        return {"message":"Item added"}
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_CONTENT, detail = "listing not found")
    
@router.delete("/{listing_id}")
def deleteFromCart(listing_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)
    result = deleteCartItem(listing_id, user['sub'])
    if result: return {"message":"Item deleted"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found in cart")

@router.put("/{listing_id}")
def editCart(cartData:CartData, listing_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)
    if cartData.amount < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount cannot be negative")
    result = updateCartItem(listing_id, user['sub'], cartData.amount)
    if result: return {"message":"Item updated"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Item not found in cart")
        