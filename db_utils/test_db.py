from db_utils.connect_db import session, engine
from datetime import datetime

from server.models import ShiftState, Vehicle, DataPoint
import server.models as models


# Create a vehicle
vehicle = Vehicle(id="123", name="Starship")
session.add(vehicle)
session.commit()

# Create a datapoint
datapoint = DataPoint(
    vehicle_id="123",
    timestamp=datetime.now(),
    speed=200,
    odometer=49923.2,
    state_of_charge=50,
    elevation=130,
    shift_state_id="D"
)

session.add(datapoint)
session.commit()