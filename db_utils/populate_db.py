from server import models
from server.models import ShiftStates, Vehicle, DataPoint
from server.database import engine

from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker

from datetime import datetime

# Initialize database
models.Base.metadata.create_all(bind=engine)

session = sessionmaker()(bind=engine)

# Create a vehicle
vehicle = Vehicle(id="123", name="Starship")
session.add(vehicle)
session.commit()

# Create a shift state
park = ShiftStates(id="P", name="Park")
drive = ShiftStates(id="D", name="Drive")
neutral = ShiftStates(id="N", name="Neutral")
reverse = ShiftStates(id="R", name="Reverse")

session.add_all([park, drive, neutral, reverse])
session.commit()

# Create a datapoint
datapoint = DataPoint(
    vehicle_id="123",
    timestamp=datetime.now(),
    speed=0,
    odometer=0,
    state_of_charge=0,
    elevation=0,
    shift_state_id="P"
)

session.add(datapoint)
session.commit()



