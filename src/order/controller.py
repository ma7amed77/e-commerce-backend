from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.exc import IntegrityError
from typing import List

from ..schema import CartEmpty, OutOfStock
from .service import fetchOrders, fetchOrderItems, createOrder
from .model import CreateOrder, OrderData, OrderItemData
from ..auth.service import verifyJWT

router= APIRouter(prefix="/order",tags=['Order'])

@router.get("/",response_model=List[OrderData])
def getOrders(auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchOrders(user)

@router.get("/{order_id}",response_model=List[OrderItemData])
def getOrderItems(order_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchOrderItems(order_id, user)

@router.post("/{order_id}",response_model=List[OrderItemData])
def createAnOrder(order_id:int, order_data:CreateOrder, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    try:
        result = createOrder(user_id=user,
                        location=order_data.location,
                        payment=order_data.payment,
                        payment_method=order_data.payment_method)
        return {"order_id":result, "message":'Order succeeded'}
    except CartEmpty as e:
        raise HTTPException(400, detail = e)
    except OutOfStock as e:
        raise HTTPException(400, detail = e)
    except IntegrityError:
        raise HTTPException(400, detail = "Order Failed")