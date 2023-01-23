from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Pydantic models used for API responses

class Vehicle(BaseModel):
    """ Vehicle information """
    id: str
    name: str
    
    class Config:
        orm_mode = True

class ShiftState(BaseModel):
    """ Vehicle shift or gear state """
    id: str
    name: str
    
    class Config:
        orm_mode = True

class Datapoint(BaseModel):
    """ Vehicle data from a specific timestamp """

    id: int
    vehicle_id: str
    timestamp: datetime
    speed: Optional[int] = None
    odometer: Optional[float] = None
    state_of_charge: Optional[int] = None
    elevation: Optional[int] = None
    shift_state: Optional[ShiftState] = None

    class Config:
        orm_mode = True