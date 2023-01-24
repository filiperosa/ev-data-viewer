from fastapi import Query, File, UploadFile
from sqlalchemy import desc, asc
from sqlalchemy.orm import Session, joinedload
# from server import schemas
from typing import List, Tuple, Union
from enum import Enum
from datetime import datetime

import server.models as md


def get_vehicle_data(db: Session, from_date: datetime = None, to_date: datetime = None, order: Union[asc, desc] = asc):
    """
    Get all vehicles datapoints
    """

    query = db.query(md.DataPoint)

    # retrieve datapoints from a specific datetime range
    if from_date:
        query = query.filter(md.DataPoint.timestamp >= from_date)
    if to_date:
        query = query.filter(md.DataPoint.timestamp <= to_date)

    query = query.order_by(order(md.DataPoint.timestamp))
    
    return query.all()


def get_vehicle_data_by_id(db: Session, id: str, from_date: datetime = None, to_date: datetime = None, order: Union[asc, desc] = asc):
    """
    Get datapoints from a specific vehicle
    """

    query = db.query(md.DataPoint).filter(md.DataPoint.vehicle_id == id)

    # retrieve datapoints from a specific datetime range
    if from_date:
        query = query.filter(md.DataPoint.timestamp >= from_date)
    if to_date:
        query = query.filter(md.DataPoint.timestamp <= to_date)
    
    query = query.order_by(order(md.DataPoint.timestamp))
    
    return query.all()


def get_vehicles(db: Session, order: Union[asc, desc] = asc):
    """
    Get all the vehicles
    """

    return db.query(md.Vehicle).order_by(order(md.Vehicle.id)).all()


def import_vehicle_data_from_csv_file(db: Session, file: UploadFile):
    """
    Upload a CSV file with vehicle data
    """

    vehicle_id = file.filename.split('.')[0]

    # check if the vehicle already exists
    # if not, create it
    new_vehicle = False
    vehicle = db.query(md.Vehicle).get(vehicle_id)
    if not vehicle:
        vehicle = md.Vehicle(id=vehicle_id)
        db.add(vehicle)
        new_vehicle = True
    
    # read the first line containing the header
    file.file.readline()

    # track number of datapoints added and skipped
    skipped = 0
    added = 0
    
    file.file.readline()
    for line in file.file.readlines():
        datapoint = new_datapoint_from_line(line)
        if not datapoint:
            continue

        if new_vehicle:
            vehicle.datapoints.append(datapoint)
            added += 1
        else:
            exists = db.query(md.DataPoint).filter(md.DataPoint.timestamp == datapoint.timestamp, md.DataPoint.vehicle_id == vehicle_id).count()
            if not exists:
                vehicle.datapoints.append(datapoint)
                added += 1
            else:
                skipped += 1
                print(f"Datapoint with timestamp {datapoint.timestamp} already exists. Skipping...")

    db.commit()

    return {
        'filename': f'{file.filename}',
        'filetype': f'{file.content_type}',
        'total_items': f'{added + skipped}',
        'items_added': f'{added}',
        'items_skipped': f'{skipped}'
        }


def new_datapoint_from_line(line) -> Union[md.DataPoint, None]:
    line = line.decode('utf-8').strip().split(',')
    if len(line) != 6:
        return None
        
    try:
        return md.DataPoint(
            timestamp=datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f") if parse_cell(line[0]) else None,
            speed=int(line[1]) if parse_cell(line[1]) else None,
            odometer=float(line[2]) if parse_cell(line[2]) else None,
            state_of_charge=int(line[3]) if parse_cell(line[3]) else None,
            elevation=int(line[4]) if parse_cell(line[4]) else None,
            shift_state_id=line[5] if parse_cell(line[5]) else None,
        )
    except Exception as e:
        print(f"Error parsing line: {line}")
        print(e)
        return None



def parse_cell(cell: str):
    """Check if a string is NULL and return None if it is"""

    if cell == "NULL":
        return None
    return cell