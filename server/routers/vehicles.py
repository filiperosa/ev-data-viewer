from fastapi import HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from server.database import get_db

router = APIRouter()

@router.get("/vehicle_data")
async def get_vehicle_data(db: Session = Depends(get_db)):
    """
    Get all vehicles datapoints
    """

    return {"message": "Hello World"}


@router.get("/vehicle_data/{id}")
async def get_vehicle_data_by_id(id: str, db: Session = Depends(get_db)):
    """
    Get datapoints from a specific vehicle
    """

    return {"message": f"Hello {id}"}
