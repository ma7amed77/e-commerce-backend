from sqlalchemy import select, func, and_

from ..schema import carts, listings, CartEmpty, OutOfStock, orders, order_item, items

def createOrder(conn, user_id:int, location:str, payment:str, payment_method:str):
        select_statement = select(
                                carts.c.amount.label("quantity"),
                                listings.c.listing_id,
                                listings.c.price,
                                listings.c.amount.label("stock"),
                                (carts.c.amount * listings.c.price).label("total_price"),
                                ).where(
                                    carts.c.user_id == user_id,
                                    carts.c.amount > 0,
                                ).join(listings, carts.c.listing_id == listings.c.listing_id
                                       ).with_for_update()
        
        rows = conn.execute(select_statement).mappings().all()

        if not rows:
            raise CartEmpty("Cart is empty")
        
        order_total = sum(row["total_price"] for row in rows)


        # Should check and handle payment here


        
        order_id = conn.execute(
            orders.insert()
            .values(user_id=user_id, state=1,payment = payment_method, location=location)
            .returning(orders.c.order_id)
        ).scalar()
        
        order_items_dicts = [{
                            "order_id":order_id,
                            "listing_id":row["listing_id"],
                            "amount":row["quantity"]
                            } 
                            for row in rows
                            ]
        conn.execute(order_item.insert(), order_items_dicts)
        
        for row in rows:
            conn.execute(
                listings.update()
                .where(listings.c.listing_id == row["listing_id"])
                .values(amount=listings.c.amount - row["quantity"])
            )
        conn.execute(carts.delete().where(and_(carts.c.user_id == user_id,carts.c.amount > 0)))
        return order_id


def fetchOrders(conn, user_id):
    statement = select(
                    orders.c.order_id,
                    orders.c.state,
                    orders.c.location,
                    orders.c.payment,
                    ).where(orders.c.user_id==user_id)
    return conn.execute(statement).mappings().all()
    
def fetchOrderItems(conn, order_id, user_id):
    statement = select(
                        items.c.item_id,
                        items.c.name,
                        items.c.description,
                        order_item.c.amount
                    ).join(orders, order_item.c.order_id==orders.c.order_id
                    ).join(listings, order_item.c.listing_id == listings.c.listing_id
                    ).join(items, listings.c.item_id==items.c.item_id
                    ).where(orders.c.user_id==user_id
                    ).where(orders.c.order_id == order_id)
    return conn.execute(statement).mappings().all()