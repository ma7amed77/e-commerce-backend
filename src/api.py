from fastapi import FastAPI

from .auth.controller import router as auth_router
from .user.controller import review_router
from .listing.controller import router as listing_router
from .cart.controller import router as cart_router
from .item.controller import router as item_router
from .seller.controller import router as seller_router
from .search.controller import router as search_router

def register_routers(app: FastAPI):
    app.include_router(search_router)
    app.include_router(auth_router)
    app.include_router(seller_router)
    app.include_router(item_router)
    app.include_router(listing_router)
    app.include_router(cart_router)
    app.include_router(review_router)