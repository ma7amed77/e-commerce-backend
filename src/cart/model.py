from pydantic import BaseModel, Field

# ------------- carts ------------- #
class CartData(BaseModel):
    amount:int =Field(description="new amount to set")