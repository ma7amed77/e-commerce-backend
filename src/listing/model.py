from pydantic import BaseModel, Field

# ------------- listing ------------- #
class ListingID(BaseModel):
    listing_id:int = Field(description="Id of the listing")

class ListingData(BaseModel):
    item_id:int = Field(description = "Id of the item to add a listing for")
    price:int = Field(description = "Item price in 0.01 units $1.00 => 100 in this", examples=["1000"])
    amount:int = Field(description = "How many items are the seller selling")

class ListingUpdateData(BaseModel):
    price:int | None = Field(description = "Item price in 0.01 units $1.00 => 100 in this")
    amount:int | None  = Field(description = "How many items are the seller selling")
