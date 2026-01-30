from sqlalchemy import select, and_, exists

from ..schema import addresses, engine

def fetchLocations(user_id:int):
    statement = select(
                    addresses.c.address_id, 
                    addresses.c.location
                    ).where(addresses.c.user_id == user_id)
    with engine.connect() as conn:
        return conn.execute(statement).mappings().all()

def addLocation(user_id:int, location:str):
    statement = addresses.insert().values(user_id=user_id, location=location).returning(addresses.c.address_id)
    with engine.begin() as conn:
        return conn.execute(statement).scalar_one()

def updateLocation(user_id:int, location:str, address_id:int):
    statement = addresses.update(
                            ).values(
                                location=location
                            ).where(
                                and_(
                                    addresses.c.user_id==user_id,
                                    addresses.c.address_id==address_id
                                )).returning(addresses.c.address_id)
    with engine.begin() as conn:
        return conn.execute(statement).scalar_one_or_none()

def deleteLocation(user_id:int, address_id:int):
    statement = addresses.delete(
                            ).where(
                                and_(
                                    addresses.c.user_id==user_id,
                                    addresses.c.address_id==address_id
                                )).returning(addresses.c.address_id)
    with engine.begin() as conn:
        return conn.execute(statement).scalar_one_or_none()  