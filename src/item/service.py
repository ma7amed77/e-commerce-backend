from sqlalchemy import select, func, and_, exists

from ..schema import engine,  items, EmptyUpdate, ratings, orders, order_item, listings, sellers, users

#---------------------- Items----------------------#
def addItem(name, description, category_id, lister_id):
    values = {"name":name,
              "description":description,
              "category_id":category_id,
              "lister_id":lister_id,}
    statement = items.insert().values(values).returning(items.c.item_id)
    with engine.begin() as conn:
        result = conn.execute(statement).scalar_one()
        return result
    
def editItem(item_id, lister_id, **kwargs):
    if not kwargs: raise EmptyUpdate("No data to update")
    statement = items.update(
                    ).where(and_(items.c.item_id==item_id, items.c.lister_id==lister_id)
                    ).values(**kwargs).returning(items.c.item_id)
    with engine.begin() as conn:
        result = conn.execute(statement).scalar_one_or_none()
        return result

def deleteItem(item_id, lister_id):
    statement = items.update(
                    ).where(
                        and_(
                            items.c.item_id==item_id,
                              items.c.lister_id==lister_id
                            )
                    ).values(item_state = 0).returning(items.c.item_id)
    
    with engine.begin() as conn:
        return conn.execute(statement).scalar_one_or_none()
    

def checkCanReview(user_id, item_id):
    return select(
        exists(
            select(1)
            .select_from(
                order_item
                .join(orders, order_item.c.order_id == orders.c.order_id)
                .join(listings, order_item.c.listing_id == listings.c.listing_id)
            )
            .where(
                and_(
                    listings.c.item_id == item_id,
                    orders.c.user_id == user_id,
                    orders.c.state != 0
                )
            )
        )
    )

def fetchItem(item_id:int, user_id:int=0):
    can_review = 0
    data_statement = select(
                  items.c.name,
                  items.c.description,
                  items.c.item_id,
                  items.c.category_id,
                  func.coalesce(func.avg(ratings.c.rating), 0).label("rating"),
                  func.count(ratings.c.rating).label("ratings")
                  ).where(items.c.item_id==item_id
                  ).outerjoin(ratings,ratings.c.item_id == items.c.item_id
                  ).group_by(items.c.item_id)
    
    listings_statement = select(listings.c.listing_id,listings.c.seller_id,sellers.c.seller_name,listings.c.price).where(and_(listings.c.item_id==item_id,listings.c.state==1)).join(sellers,listings.c.seller_id==sellers.c.seller_id).order_by(listings.c.price)
    reviews_statement = select(ratings.c.rating, ratings.c.review, users.c.name).where((ratings.c.item_id==item_id)&(ratings.c.review!=None)).outerjoin(users,ratings.c.user_id ==users.c.user_id)
    check_can_review_statement = checkCanReview(user_id, item_id)
    with engine.connect() as conn:
        item_data = conn.execute(data_statement).fetchone()
        if item_data:
            item_listings = conn.execute(listings_statement).mappings().all()
            item_reviews = conn.execute(reviews_statement).mappings().all()
            if user_id > 0:
                if conn.execute(check_can_review_statement).scalar(): can_review = 1

            return {**(item_data._mapping),"listings":item_listings, "reviews":item_reviews, "can_review":can_review}
        return None