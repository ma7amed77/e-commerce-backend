from pydantic import BaseModel, Field
from ..auth.model import Token


# ------------- seller ------------- #
class BecomeSeller(BaseModel):
    name: str = Field(min_length=3, description="shop name", examples=["Seller Name"])

class SellerID(Token):
    pass

class SellerItem(BaseModel):
    item_id:int = Field(description="Id of the item")
    name:str = Field(description="Name of the item")
    item_state:int = Field(description="Is this item deleted")

class SellerListing(SellerItem):
    listing_id:int = Field(description="Id of the listing")
    state:int = Field(description="Is this listing deleted")
    price:int = Field(description = "Item price in 0.01 units $1.00 => 100 in this")
    amount:int = Field(description = "How many items are the seller selling")
