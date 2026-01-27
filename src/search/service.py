from sqlalchemy import select, func, and_, distinct, or_

from ..schema import engine,  items, listings, ratings, categories

#---------------------- Items Search & filter ----------------------#
def searchItems(statement, search:str):
    keyWord = "%"+search.strip().replace(" ","%")+"%" 
    return statement.where(or_(items.c.name.ilike(keyWord),items.c.description.ilike(keyWord)))
  
def fillData(base):
    return select(base.c.name,
                  base.c.description,
                  base.c.item_id,
                  base.c.category_id,
                  func.min(listings.c.price).label("price_min"),
                  func.max(listings.c.price).label("price_max"),
                  func.count(listings.c.price).label("amount"),
                  func.coalesce(func.avg(ratings.c.rating), 0).label("rating"),
                  func.count(ratings.c.rating).label("ratings")
                 ).select_from(
                     base.outerjoin(listings,and_(listings.c.item_id == base.c.item_id, listings.c.state == 1)
                        ).outerjoin(ratings, ratings.c.item_id == base.c.item_id)).group_by(base.c.item_id)

def getSearchCategories(statement):
    sq = statement.subquery()
    return select(distinct(sq.c.category_id), categories.c.name).join(categories, categories.c.category_id == sq.c.category_id)

def filterListings(statement, rating, category, price_min, price_max):
    sq = statement.subquery()
    conditions = []
    if rating != 0:
        conditions.append(sq.c.rating >= rating)
    if (price_min != 0): 
        conditions.append(or_(sq.c.price_min>=price_min, sq.c.price_max>=price_min))
    if (price_max != 0):
        conditions.append(or_(sq.c.price_min<=price_max, sq.c.price_max<=price_max))
    
    if category is not None:
        conditions.append(sq.c.category_id==category)
    return sq.select().where(and_(*conditions)).order_by(sq.c.item_id)

def fetchList(page=0, limit=10,search = "", rating:int = 0, category=None, price_min:int = 0, price_max:int = 0):
    statement = None
    if search != "" :
        statement = fillData(searchItems(items.select(), search).subquery())
    else:
        statement = fillData(items) 
    categories = getSearchCategories(statement)
    statement = filterListings(statement, rating, category, price_min, price_max)
    statement = statement.limit(limit).offset(page*limit)
    with engine.connect() as conn:
        categories_rows = conn.execute(categories).mappings().all()
        items_rows = conn.execute(statement).mappings().all()
        return {"items":items_rows, "categories":categories_rows}
