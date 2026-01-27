from pydantic import BaseModel, Field

# ------------- Review ------------- #
class RatingData(BaseModel):
    rating:int = Field(description="Rating in numbers from 1 to 5", examples=["1"])
    review:str|None = Field(description="Review and can be empty", examples=["This item is good"])
