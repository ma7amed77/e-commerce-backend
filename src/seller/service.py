from sqlalchemy import select

from ..schema import  listings, d_insert, sellers, items

# ------------ Sellers ------------- #
def registerSeller(conn, user_id, seller_name):
    statement = d_insert(sellers).values(
                            seller_name=seller_name,
                            user_id=user_id).on_conflict_do_update( 
                            index_elements=[sellers.c.user_id],
                            set_={"seller_name": seller_name}).returning(sellers.c.seller_id)
    
    result = conn.execute(statement)
    return result.scalar_one()
    
def fetchSeller(conn, user_id):
    statement = select(sellers.c.seller_id).where(sellers.c.user_id==user_id)
    return conn.execute(statement).scalar_one_or_none()

def fetchSellerListings(conn, seller_id):
    statement = select(listings.c.listing_id, 
                       items.c.item_id, 
                       items.c.name,
                       items.c.item_state,
                       listings.c.state,
                       listings.c.price,
                       listings.c.amount
                       ).where(listings.c.seller_id==seller_id
                               ).select_from(listings.join(items, listings.c.item_id==items.c.item_id))
    return conn.execute(statement).mappings().all()

def fetchSellerItems(conn, seller_id):
    statement = select(items.c.item_id, 
                       items.c.name,
                       items.c.item_state
                       ).where(items.c.lister_id==seller_id)
    return conn.execute(statement).mappings().all()