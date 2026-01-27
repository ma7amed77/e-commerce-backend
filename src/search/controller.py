from fastapi import APIRouter

from .service import fetchList
from .model import ListData
from ..auth.service import verifySeller

router= APIRouter(prefix="/search",tags=['Search'])

# ------------- items ------------- #
@router.get("/", response_model=ListData)
def getItems(page:int=0, limit:int=10, search = "", rating:int=0, category=None, price_min:int = 0, price_max:int = 0):
    return fetchList(page, limit,search, rating, category, price_min, price_max)
