# FastApi e-commerce

This is a mini amazon like api built with FastApi and SQLalchemy core. The project is built as an application for complex quarries and quarry optmizations.

## Interactive api doc (readonly database)

[Interactive api doc](https://e-commerce-backend-ma7amed77143-7mh2cnla.leapcell.dev/docs)

(clone the project to test adding and ordring)

It doesn't have content filtring so I can't leave it open on the internet 😄

### Some Testing data

* alice@example.com
* hashed_password_1
*
* bob@example.com
* hashed_password_2
*
* charlie@example.com
* hashed_password_3

## How is it structured

![1769564662455](images/README/1769564662455.png)

### Items

Items include name and general data about the item.
* Multiple sellers can sell the same item
* Items are created once, listings define price & stock

### Lists
#### Listings represent:
* Price
* Stock
* Seller

Lists is like a price and stock for items. Each seller can add as many listings for same items so sellers selling known items can just add a listing for an exsiting item. Or a company can list thier items with specs and sellers just add a listing with thier price.

### Users & Sellers

Usually it will requier manaual checking for legal papers to become a seller, but as this is for showcase users can just add a shop name will providing thier login jwt token to become a seller. (if api called again it will just update the name)

### Ratings & reviews

Users can rate items can have an option to leave a review

To leave a review user must have an order with this item

### Carts

Carts are connected to listings not items as user can choose which price/seller to buy item from.

User can:

* Add item to cart (if item in cart it will add one).
* Update a card with new amount.
* Remove the listing.

### Locations

locations are more of a save system so user doesn't have to rewrite the location in each order

### Items Page & Search

Items page and search collects data from Items and ratings and prices and seller name from Listings. There data is then used to filter and search

## Database

The project started with SQLite for faster dev but for production a server based sql like PostgreSQL is a must, as SQLitesqlite doesn't have row locking so the whole database will be locked when ordring. also SQLitesqlite doesn't support async oprations.

## Authentication

I use jwt and store user_id and seller_id if it's a seller too

The project doesn't have password hashing as this is a showcase for the systems so DO NOT USE REAL DATA please 😄
