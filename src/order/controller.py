from fastapi import APIRouter, HTTPException, Header
from sqlalchemy.exc import IntegrityError
from typing import List

from ..schema import CartEmpty, OutOfStock, get_conn
from .service import fetchOrders, fetchOrderItems, createOrder
from .model import CreateOrder, OrderData, OrderItemData, OrderCompleted
from ..auth.service import verifyJWT

router= APIRouter(prefix="/order",tags=['Order'])

@router.get("/",response_model=List[OrderData])
def getOrders(conn:get_conn, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchOrders(conn, user)

@router.get("/{order_id}",response_model=List[OrderItemData])
def getOrderItems(conn:get_conn, order_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchOrderItems(conn, order_id, user)

@router.post("/",response_model=OrderCompleted)
def createAnOrder(conn:get_conn, order_data:CreateOrder, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    try:
        result = createOrder(
                        conn,
                        user_id=user,
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