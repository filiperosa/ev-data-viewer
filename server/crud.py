from fastapi import Query
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session, joinedload
# from server import schemas
from typing import List, Tuple, Union
from enum import Enum
from datetime import datetime

import server.models as md


def get_vehicle_data(db: Session, order: Union[asc, desc] = asc, page: int = 1, limit: int = 50):
    """
    Get all vehicles datapoints
    """

    return db.query(md.DataPoint).order_by(order(md.DataPoint.timestamp)).offset((page - 1) * limit).limit(limit).all()


def get_vehicle_data_by_id(db: Session, id: str, order: Union[asc, desc] = asc, page: int = 1, limit: int = 50):
    """
    Get datapoints from a specific vehicle
    """

    return db.query(md.DataPoint).filter(md.DataPoint.vehicle_id == id).order_by(order(md.DataPoint.timestamp)).offset((page - 1) * limit).limit(limit).all()