from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, ForeignKey, CheckConstraint, Index, text
from sqlalchemy.dialects.sqlite import insert as d_insert

engine = create_engine("sqlite:///database.db", echo=True)

meta = MetaData()

class CannotReview(Exception):
    pass
class EmptyUpdate(Exception):
    pass

categories = Table("categories",meta,
                   Column("category_id",Integer,primary_key=True),
                   Column("name", String, nullable=False, unique=True)
                   )

users = Table("users",meta,
              Column("user_id", Integer, primary_key=True),
              Column("name", String, nullable=False),
              Column("email", String, nullable=False, unique=True),
              Column("password", String, nullable=False),
              )

sellers = Table("sellers",meta,
                Column("seller_id", Integer,primary_key=True),
                Column("user_id", Integer, ForeignKey("users.user_id"), unique = True),
                Column("seller_name", String, nullable=False),
                )
Index("ix_seller_user_id",sellers.c.user_id)

items = Table("items",meta,
              Column("item_id", Integer, primary_key=True),
              Column("name", String, nullable=False),
              Column("description", String, nullable=False),
              Column("category_id", Integer, ForeignKey("categories.category_id")),
              Column("lister_id", Integer, ForeignKey("sellers.seller_id")), # this is for wanting to edit item
              Column("item_state", Integer, server_default=text("1"), nullable=False), # 1-available 0-unlisted
              )
Index("ix_item_lister_id", items.c.lister_id)

listings = Table("listings",meta,
                 Column("listing_id", Integer, primary_key=True),
                 Column("seller_id", Integer, ForeignKey("sellers.seller_id")),
                 Column("item_id", Integer, ForeignKey("items.item_id")),
                 Column("price", Integer, nullable=False), # price in 0.01 of used unit
                 Column("state", Integer,server_default=text("1"), nullable = False), # 1-available 0-unlisted
                 Column("amount", Integer, nullable=False),
                 CheckConstraint('amount >= 0',name="amount_check")
                 )
Index("ix_listings_item_state_price",listings.c.item_id, listings.c.state, listings.c.price)

carts = Table("carts",meta,
              Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
              Column("listing_id", Integer, ForeignKey("listings.listing_id"), primary_key=True),
              Column("amount", Integer, default=1),
              CheckConstraint('amount >= 0',name="amount_check"),
              )

addresses = Table("addresses",meta,
                Column("address_id", Integer, primary_key=True),
                Column("user_id", Integer, ForeignKey("users.user_id")),
                Column("location", String, nullable=False)
                  )
Index("ix_addresses_userid", addresses.c.user_id)

orders = Table("orders",meta,
               Column("order_id",Integer, primary_key = True),
               Column("user_id", Integer, ForeignKey("users.user_id")),
               Column("location", String, nullable=False),
               Column("state", Integer, default=1), # 0-Canceled 1-initiated 2-in-the-way 3-delivered
               Column("payment", String, nullable=False),
               )
Index("ix_orders_userid", orders.c.user_id)

order_item = Table("order_item",meta,
               Column("order_id",Integer, ForeignKey("orders.order_id")),
               Column("listing_id", Integer, ForeignKey("listings.listing_id")),
               Column("amount", Integer, nullable=False),
               )
Index("ix_orderItem_order_id", order_item.c.order_id)

ratings = Table("ratings",meta,
                Column("rating", Integer, nullable=False), # 1-5 rating
                Column("user_id", Integer, ForeignKey("users.user_id"), primary_key=True),
                Column("item_id", Integer, ForeignKey("items.item_id"), primary_key=True),
                Column("review", String, default=''),
                )
Index("ix_itemId_rating", ratings.c.item_id, ratings.c.rating)

meta.create_all(engine)
