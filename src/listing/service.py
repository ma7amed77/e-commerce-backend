from sqlalchemy import select, func, and_

from ..schema import engine,  listings, d_insert, EmptyUpdate

#---------------------- Items listing ----------------------#
def addListing(seller_id, item_id, price, amount):
    values = {"item_id":item_id,
              "price":price,
              "amount":amount,
              "seller_id":seller_id}
    statement = listings.insert().values(values).returning(listings.c.listing_id)
    with engine.begin() as conn:
        result = conn.execute(statement).scalar_one()
        return result

def editListing(seller_id, listing_id, **kwargs):
    if not kwargs: raise EmptyUpdate("No data to update")
    statement = listings.update(
                    ).where(and_(listings.c.listing_id==listing_id, listings.c.seller_id==seller_id)
                    ).values(**kwargs).returning(listings.c.listing_id)
    with engine.begin() as conn:
        result = conn.execute(statement).scalar_one_or_none()
        return result

def deleteListing(seller_id, listing_id):
    statement = listings.update(
                    ).where(and_(listings.c.listing_id==listing_id, listings.c.seller_id==seller_id)
                    ).values(state = 0).returning(listings.c.listing_id)
    with engine.begin() as conn:
        return conn.execute(statement).scalar_one_or_none()
