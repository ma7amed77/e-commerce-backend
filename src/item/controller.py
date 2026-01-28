from fastapi import APIRouter, HTTPException, status, Header
from sqlalchemy.exc import IntegrityError

from .service import addItem, EmptyUpdate, fetchItem, editItem, deleteItem
from .model import ItemData, ItemUpdateData, ItemID, PageItemData
from ..auth.service import verifySeller

router= APIRouter(prefix="/items",tags=['Item'])


@router.get("/{item_id}",response_model = PageItemData)
def getItem(item_id:int):
    result = fetchItem(item_id)
    if not result:
        raise HTTPException(404, "Item not found")
    return result

@router.post("/", response_model=ItemID)
def listItem(itemData:ItemData, auth: str = Header(None)):
    try:
        seller = verifySeller(auth)
        result = addItem(lister_id=seller, **itemData.model_dump())
        return ItemID(item_id = result)
    except IntegrityError:
        raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = "Category ID is not valid")

@router.patch("/{item_id}", response_model=ItemID)
def patchAnItem(itemData:ItemUpdateData, item_id:int, auth: str = Header(None)):
    try:
        seller = verifySeller(auth)
        result = editItem(item_id=item_id, lister_id=seller, **itemData.model_dump())
        if result:
            return ItemID(item_id = result)
        else: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no item with id:{item_id} found for seller")
    except EmptyUpdate as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.delete("/{item_id}")
def deleteAnItem(item_id:int, auth: str = Header(None)):
    seller = verifySeller(auth)
    result = deleteItem(item_id = item_id, lister_id = seller)
    if result:
        return {"message":"Item has been deleted"}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"no item with id:{item_id} found for this seller")

     