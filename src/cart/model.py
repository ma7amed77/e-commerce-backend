from pydantic import BaseModel, Field

# ------------- carts ------------- #
class CartUpdate(BaseModel):
    amount:int =Field(description="new amount to set")

class CartData(BaseModel):
    listing_id:int
    item_id:int
    price:int
    state:int
    name:str
    description:str
    rating:float
    ratings:int