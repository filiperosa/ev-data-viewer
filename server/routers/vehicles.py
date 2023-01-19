from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from server.database import get_db
from server import crud

from typing import Union 
from enum import Enum

router = APIRouter()

class OrderByEnum(str, Enum):
    asc = 'asc'
    desc = 'desc'


@router.get("/vehicle_data")
def get_vehicle_data(db: Session = Depends(get_db), order: OrderByEnum = OrderByEnum.asc, page: int = 1, limit: int = 50):
    """
    Get all vehicles datapoints
    """

    return crud.get_vehicle_data(db, eval(order), page, limit)


@router.get("/vehicle_data/{id}")
def get_vehicle_data_by_id(id: str, db: Session = Depends(get_db), order: OrderByEnum = OrderByEnum.asc, page: int = 1, limit: int = 50):
    """
    Get datapoints from a specific vehicle
    """

    return crud.get_vehicle_data_by_id(db, id, eval(order), page, limit)
