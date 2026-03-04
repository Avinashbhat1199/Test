
from sqlalchemy.orm import Session
from . import models, schemas
from .utils import haversine

def create_address(db: Session, address: schemas.AddressCreate):
    db_address = models.Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_addresses(db: Session):
    return db.query(models.Address).all()

def get_address(db: Session, address_id: int):
    return db.query(models.Address).filter(models.Address.id == address_id).first()

def update_address(db: Session, address_id: int, address: schemas.AddressUpdate):
    db_address = get_address(db, address_id)
    if db_address:
        for key, value in address.dict().items():
            setattr(db_address, key, value)
        db.commit()
        db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int):
    db_address = get_address(db, address_id)
    if db_address:
        db.delete(db_address)
        db.commit()
    return db_address

def get_addresses_within_distance(db: Session, lat: float, lon: float, distance_km: float):
    addresses = get_addresses(db)
    return [
        addr for addr in addresses
        if haversine(lat, lon, addr.latitude, addr.longitude) <= distance_km
    ]
