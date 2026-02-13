from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import IntegrityError

from .service import addListing, editListing, EmptyUpdate, deleteListing
from .model import ListingData, ListingUpdateData, ListingID
from ..auth.service import verifySeller
from ..schema import get_conn

router= APIRouter(prefix="/listing",tags=['Listing'])

# ------------- listings ------------- #
@router.post("/", response_model=ListingID)
def listListing(conn:get_conn, listingData:ListingData, auth: str = Header(None)):
    try:
        seller = verifySeller(auth)
        result = addListing(conn, seller_id=seller, **listingData.model_dump())
        return ListingID(listing_id = result)
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Invalid seller id or item id")

@router.patch("/{listing_id}", response_model=ListingID)
def patchAListing(conn:get_conn, listingData:ListingUpdateData, listing_id:int, auth: str = Header(None)):
    try:
        seller = verifySeller(auth)
        result = editListing(conn, listing_id=listing_id, seller_id=seller, **listingData.model_dump())
        if result:
            return ListingID(listing_id = result)
        else: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no listing with id:{listing_id} found for this seller")
    except EmptyUpdate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{listing_id}")
def deleteAListing(conn:get_conn, listing_id:int, auth: str = Header(None)):
    seller= verifySeller(auth)
    result = deleteListing(conn, listing_id=listing_id, seller_id=seller)
    if result:
        return {"message":"Listing has been deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no listing with id:{listing_id} found for this seller")

        