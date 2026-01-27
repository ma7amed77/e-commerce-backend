from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import IntegrityError

from .service import addListing, editListing, EmptyUpdate, deleteListing
from .model import ListingData, ListingUpdateData, ListingID
from ..auth.service import verifySeller

router= APIRouter(prefix="/listing",tags=['Listing'])

# ------------- listings ------------- #
@router.post("/", response_model=ListingID)
def listListing(listingData:ListingData, auth: str = Header(None)):
    try:
        seller_data = verifySeller(auth)
        result = addListing(seller_id=seller_data['seller_id'], **listingData.model_dump())
        return ListingID(listing_id = result)
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Invalid seller id or item id")

@router.patch("/{listing_id}", response_model=ListingID)
def patchAListing(listingData:ListingUpdateData, listing_id:int, auth: str = Header(None)):
    try:
        seller_data = verifySeller(auth)
        result = editListing(listing_id=listing_id, seller_id=seller_data['seller_id'], **listingData.model_dump())
        if result:
            return ListingID(listing_id = result)
        else: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no listing with id:{listing_id} found for this seller")
    except EmptyUpdate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{listing_id}", response_model=ListingID)
def deleteAListing(listing_id:int, auth: str = Header(None)):
    seller_data = verifySeller(auth)
    result = deleteListing(listing_id=listing_id, seller_id=seller_data['seller_id'])
    if result:
        return {"message":"Listing has been deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no listing with id:{listing_id} found for this seller")

        