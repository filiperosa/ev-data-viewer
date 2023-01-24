from fastapi import HTTPException, APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from server.database import get_db
from server import crud, schemas
from datetime import datetime

from fastapi_pagination import Page, paginate

from typing import Union, List
from enum import Enum

router = APIRouter()

class OrderByEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'


@router.get("/vehicle_data", response_model=Page[schemas.Datapoint])
def get_vehicle_data(db: Session = Depends(get_db), from_date: datetime = None , to_date: datetime = None, order: OrderByEnum = OrderByEnum.asc):
    """
    Get all vehicles datapoints
    """

    return paginate(crud.get_vehicle_data(db, from_date, to_date, eval(order)))


@router.get("/vehicle_data/{id}", response_model=Page[schemas.Datapoint])
def get_vehicle_data_by_id(id: str, db: Session = Depends(get_db), from_date: datetime = None , to_date: datetime = None, order: OrderByEnum = OrderByEnum.asc):
    """
    Get datapoints from a specific vehicle
    """

    return paginate(crud.get_vehicle_data_by_id(db, id, from_date, to_date, eval(order)))


@router.get("/vehicles", response_model=List[schemas.Vehicle])
def get_vehicles(db: Session = Depends(get_db)):
    """
    Get all the vehicle IDs
    """

    return crud.get_vehicles(db)


@router.post("/vehicle_data")
def upload_vehicle_data(file: UploadFile, db: Session = Depends(get_db)):
    return crud.import_vehicle_data_from_csv_file(db, file)