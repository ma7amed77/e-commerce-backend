from pydantic import BaseModel, Field

from typing import List

# ------------- items ------------- #
class ItemID(BaseModel):
    item_id:int = Field(description="Id of the item")

class ItemData(BaseModel):
    name:str = Field(min_length=3, description="item title or name", examples=["item name"])
    description:str = Field(min_length=3, description="item description", examples=["item can do 1 and 2 and 3"])
    category_id:int = Field(description="category id can be from 1 to what ever the last category is")

class ItemUpdateData(BaseModel):
    name:str|None = Field(min_length=3, description="item title or name", examples=["item name"])
    description:str|None = Field(min_length=3, description="item description", examples=["item can do 1 and 2 and 3"])
    category_id:int|None = Field(description="category id can be from 1 to what ever the last category is")

class PageListingData(BaseModel):
    listing_id:int
    seller_id:int
    seller_name:str
    price:int

class PageReview(BaseModel):
    rating:int
    review:str
    name:str

class PageItemData(ItemData):
    item_id:int = Field(description="Id of the item")
    rating:float = Field(description="1->5 showing average rating for this item")
    ratings:int = Field(description="How many users rated this item")
    can_review:int = Field(description="Did user buy this item before 1 -> yes  0 -> No")
    listings:List[PageListingData] = Field(description="Listings found for this item")

