from pydantic import BaseModel, Field

# ------------- seller ------------- #
class BecomeSeller(BaseModel):
    name: str = Field(min_length=3, description="shop name", examples=["Seller Name"])

class SellerID(BaseModel):
    seller_token:str = Field(description="new token that has seller id used for listing new items")

class SellerItem(BaseModel):
    item_id:int = Field(description="Id of the item")
    name:str = Field(description="Name of the item")
    item_state:int = Field(description="Is this item deleted")

class SellerListing(SellerItem):
    listing_id:int = Field(description="Id of the listing")
    state:int = Field(description="Is this listing deleted")
