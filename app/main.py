
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, SessionLocal, Base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Address Book API")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/addresses", response_model=schemas.AddressResponse)
def create_address(address: schemas.AddressCreate, db: Session = Depends(get_db)):
    return crud.create_address(db, address)

@app.get("/addresses", response_model=list[schemas.AddressResponse])
def read_addresses(db: Session = Depends(get_db)):
    return crud.get_addresses(db)

@app.put("/addresses/{address_id}", response_model=schemas.AddressResponse)
def update_address(address_id: int, address: schemas.AddressUpdate, db: Session = Depends(get_db)):
    db_address = crud.update_address(db, address_id, address)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return db_address

@app.delete("/addresses/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = crud.delete_address(db, address_id)
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"message": "Deleted successfully"}

@app.get("/addresses/nearby", response_model=list[schemas.AddressResponse])
def nearby_addresses(lat: float, lon: float, distance_km: float, db: Session = Depends(get_db)):
    return crud.get_addresses_within_distance(db, lat, lon, distance_km)
