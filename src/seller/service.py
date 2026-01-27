from sqlalchemy import select, func, and_

from ..schema import engine,  listings, d_insert, sellers, items

# ------------ Sellers ------------- #
def registerSeller(user_id, seller_name):
    statement = d_insert(sellers).values(
                            seller_name=seller_name,
                            user_id=user_id).on_conflict_do_update( 
                            index_elements=[sellers.c.user_id],
                            set_={"seller_name": seller_name}).returning(sellers.c.seller_id)
    with engine.begin() as conn:
        result = conn.execute(statement)
        return result.scalar_one()
    
def fetchSeller(user_id):
    statement = select(sellers.c.seller_id).where(sellers.c.user_id==user_id)
    with engine.connect() as conn:
        return conn.execute(statement).scalar_one_or_none()

def fetchSellerItems(seller_id):
    statement = select(listings.c.listing_id, 
                       items.c.item_id, 
                       items.c.name
                       ).where(listings.c.seller_id==seller_id
                               ).select_from(listings.join(items, listings.c.item_id==items.c.item_id))
    with engine.connect() as conn:
        return conn.execute(statement).mappings().all()

def fetchSellerListings(seller_id):
    statement = select(items.c.item_id, 
                       items.c.name
                       ).where(items.c.lister_id==seller_id)
    with engine.connect() as conn:
        return conn.execute(statement).mappings().all()