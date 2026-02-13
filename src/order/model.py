from pydantic import BaseModel, Field

class CreateOrder(BaseModel):
    location:str
    payment:str
    payment_method:str

class OrderData(BaseModel):
    order_id:int
    state:int
    location:str
    payment:str

class OrderItemData(BaseModel):
    item_id:int
    name:str
    description:str
    amount:int

class OrderCompleted(BaseModel):
    order_id:int
    message:str