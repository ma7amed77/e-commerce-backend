from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import IntegrityError

from .review_service import addRating
from .location_service import addLocation, fetchLocations, deleteLocation, updateLocation
from .model import RatingData, AddressData, AddressId
from ..auth.service import verifyJWT
from ..schema import CannotReview

# ------------- item review ------------- #
review_router = APIRouter(prefix="/review",tags=['Review'])

@review_router.post("/{item_id}")
def addARating(ratingData:RatingData, item_id:int, auth: str = Header(None)):
    user_data = verifyJWT(auth)
    try:
        addRating(item_id=item_id,user_id=user_data['sub'], **ratingData.model_dump())
        return {"message":"Review added"}
    except CannotReview:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"no item with id:{item_id} that user has bought")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Rating of {ratingData.rating} is not valid")
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Invalid user id or item id")    


# ------------- Saved Locations ------------- #
location_router = APIRouter(prefix="/address",tags=['Addresses'])

@location_router.get("/")
def getAddresses(auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchLocations(user_id=user)

@location_router.post("/")
def addAddress(address_data:AddressData, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = addLocation(user_id=user, **address_data.model_dump())
    return AddressId(address_id=result)

@location_router.put("/{address_id}")
def editAddresses(address_id:int, address_data:AddressData, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = updateLocation(user_id=user, address_id=address_id, **address_data.model_dump())
    if result : return AddressId(address_id=result)
    raise HTTPException(404, detail=f"No listing with id: {address_id} for this user")

@location_router.delete("/{address_id}")
def deleteAddresses(address_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = deleteLocation(user_id=user, address_id=address_id)
    if result : return AddressId(address_id=result)
    raise HTTPException(404, detail=f"No listing with id: {address_id} for this user")