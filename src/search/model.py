from pydantic import BaseModel, Field

from typing import List

from ..item.model import ItemData

# ------------- items ------------- #
class ListItemData(ItemData):
    item_id:int = Field(description="Id of the item")
    price_min:int = Field(description="Minimum price found for this item")
    price_max:int|None = Field(description="Maximum price found for this item")
    amount:int = Field(description="Stock left")
    rating:float = Field(description="1->5 showing average rating for this item")
    ratings:int = Field(description="How many users rated this item")
    
class Category(BaseModel):
    name:str
    category_id:int
    
class ListData(BaseModel):
    items: List[ListItemData]
    categories: List[Category]
