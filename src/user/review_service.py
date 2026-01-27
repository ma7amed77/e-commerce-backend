from sqlalchemy import select, and_, exists

from ..schema import engine,  ratings, d_insert, order_item, orders, CannotReview


#---------------------- Items reviews ----------------------#

def checkCanReview(user_id, item_id):
    return select(exists().where(and_(order_item.c.item_id==item_id, orders.c.user_id==user_id))).select_from(order_item.join(orders, order_item.c.order_id == orders.c.order_id))


def addRating(user_id:int, item_id:int, rating:int, review:str = ""):
    if rating < 1 or rating > 5 : raise ValueError("Not a valid Rating")
    indexes = {"user_id":user_id,
              "item_id":item_id}
    
    values = {"rating":rating, 
              **({"review": review} if (review.strip() != "") else {})}
    
    rating_statement = d_insert(ratings).values(**values,**indexes
                                ).on_conflict_do_update(
                                index_elements=[ratings.c.user_id,ratings.c.item_id],
                                set_= values)
    check_can_review_statement = checkCanReview(user_id, item_id)

    with engine.begin() as conn:
        can_review = conn.execute(check_can_review_statement).scalar()
        if not can_review: raise CannotReview("User has not purchased this item")
        conn.execute(rating_statement)