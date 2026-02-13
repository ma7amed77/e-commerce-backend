from fastapi import APIRouter, HTTPException, Header, status
from sqlalchemy.exc import IntegrityError

from .review_service import addRating
from .location_service import addLocation, fetchLocations, deleteLocation, updateLocation
from .model import RatingData, AddressData, AddressId
from ..auth.service import verifyJWT
from ..schema import CannotReview, get_conn

# ------------- item review ------------- #
review_router = APIRouter(prefix="/review",tags=['Review'])

@review_router.post("/{item_id}")
def addARating(conn:get_conn, ratingData:RatingData, item_id:int, auth: str = Header(None)):
    user_data = verifyJWT(auth)
    try:
        addRating(conn, item_id=item_id,user_id=user_data['sub'], **ratingData.model_dump())
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
def getAddresses(conn:get_conn, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    return fetchLocations(conn, user_id=user)

@location_router.post("/")
def addAddress(conn:get_conn, address_data:AddressData, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = addLocation(conn, user_id=user, **address_data.model_dump())
    return AddressId(address_id=result)

@location_router.put("/{address_id}")
def editAddresses(conn:get_conn, address_id:int, address_data:AddressData, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = updateLocation(conn, user_id=user, address_id=address_id, **address_data.model_dump())
    if result : return AddressId(address_id=result)
    raise HTTPException(404, detail=f"No listing with id: {address_id} for this user")

@location_router.delete("/{address_id}")
def deleteAddresses(conn:get_conn, address_id:int, auth: str = Header(None)):
    user = verifyJWT(auth)['sub']
    result = deleteLocation(conn, user_id=user, address_id=address_id)
    if result : return AddressId(address_id=result)
    raise HTTPException(404, detail=f"No listing with id: {address_id} for this user")