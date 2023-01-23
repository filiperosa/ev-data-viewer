from fastapi import Query
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session, joinedload
# from server import schemas
from typing import List, Tuple, Union
from enum import Enum
from datetime import datetime

import server.models as md


def get_vehicle_data(db: Session, from_date: datetime = None, to_date: datetime = None, order: Union[asc, desc] = asc, page: int = 1, limit: int = 50):
    """
    Get all vehicles datapoints
    """

    query = db.query(md.DataPoint)

    # retrieve datapoints from a specific datetime range
    if from_date:
        query = query.filter(md.DataPoint.timestamp >= from_date)
    if to_date:
        query = query.filter(md.DataPoint.timestamp <= to_date)

    query = query.order_by(order(md.DataPoint.timestamp)).offset((page - 1) * limit).limit(limit)
    
    return query.all()


def get_vehicle_data_by_id(db: Session, id: str, from_date: datetime = None, to_date: datetime = None, order: Union[asc, desc] = asc, page: int = 1, limit: int = 50):
    """
    Get datapoints from a specific vehicle
    """

    query = db.query(md.DataPoint).filter(md.DataPoint.vehicle_id == id)

    # retrieve datapoints from a specific datetime range
    if from_date:
        query = query.filter(md.DataPoint.timestamp >= from_date)
    if to_date:
        query = query.filter(md.DataPoint.timestamp <= to_date)
    
    query = query.order_by(order(md.DataPoint.timestamp)).offset((page - 1) * limit).limit(limit)
    
    return query.all()


def get_vehicles(db: Session, order: Union[asc, desc] = asc, page: int = 1, limit: int = 100):
    """
    Get all the vehicles
    """

    return db.query(md.Vehicle).order_by(order(md.Vehicle.id)).offset((page - 1) * limit).limit(limit).all()