from sqlalchemy import select, func, and_

from ..schema import carts, listings, items, ratings, d_insert


# ------------ Cart ------------- #
def fetchCart(conn, user_id:int):
    listings_sq = select(carts.c.amount, listings.c.listing_id, listings.c.item_id, listings.c.price, listings.c.state).where(carts.c.user_id == user_id).outerjoin(listings,carts.c.listing_id==listings.c.listing_id).subquery()
    cart_items_sq = select(listings_sq, items.c.name,items.c.description).outerjoin(items,listings_sq.c.item_id == items.c.item_id).subquery()
    rated_items_statement = select(cart_items_sq, func.coalesce(func.avg(ratings.c.rating), 0).label("rating"), 
                                   func.count(ratings.c.rating).label("ratings")).outerjoin(ratings,ratings.c.item_id == cart_items_sq.c.item_id).group_by(cart_items_sq.c.item_id)
    return conn.execute(rated_items_statement).mappings().all()

def addCartItem(conn, listing:int, user_id):
    statement = d_insert(carts).values(listing_id=listing,
                           user_id=user_id,
                           amount=1).on_conflict_do_update( 
                            index_elements=[carts.c.user_id, carts.c.listing_id],
                            set_={"amount": carts.c.amount + 1})
    conn.execute(statement)
            
def deleteCartItem(conn, listing:int, user_id):
    statement = carts.delete().where(and_(carts.c.user_id==user_id,carts.c.listing_id==listing))
    result = conn.execute(statement)
    return result.rowcount > 0

def updateCartItem(conn, listing:int, user_id, amount:int):
    statement = carts.update().where(and_(carts.c.user_id==user_id,carts.c.listing_id==listing)).values(amount=amount)
    result = conn.execute(statement)
    return result.rowcount > 0
