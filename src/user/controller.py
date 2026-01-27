from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import IntegrityError

from .review_service import addRating
from .model import RatingData
from ..auth.service import verifyJWT
from ..schema import CannotReview

# ------------- item review ------------- #
review_router = APIRouter(prefix="/review",tags=['Review'])

@review_router.post("/{item_id}")
def addARating(ratingData:RatingData, item_id:int, auth: str = Header(None)):
    user_data = verifyJWT(auth)
    try:
        addRating(user_id=user_data['sub'], **ratingData.model_dump())
        return {"message":"Review added"}
    except CannotReview:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"no item with id:{item_id} that user has bought")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Rating of {ratingData.rating} is not valid")
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Invalid user id or item id")    