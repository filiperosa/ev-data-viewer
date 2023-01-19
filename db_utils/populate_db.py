### Populate from the csv files

import os
from datetime import datetime

from db_utils.connect_db import session
from server.models import DataPoint, Vehicle, ShiftState
import server.models as models

def parse_cell(cell: str):
    """Check if a string is NULL and return None if it is"""

    if cell == "NULL":
        return None
    return cell
    

# create a vehicle for each csv filename
for file in os.listdir("db_utils/data/"):
    if file.endswith(".csv"):
        # create a new vehicle
        
        vehicle = Vehicle(id=file.split(".csv")[0], name="")
        
        # open the csv and add vehicle datapoints

        with open(f"db_utils/data/{file}", "r") as f:
            # consume the 1st line containing the header
            first_line = f.readline()

            # for each line create a vehicle datapoint
            for line in f:
                line = line.strip().split(",")
                datapoint = DataPoint(
                    timestamp=datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S.%f") if parse_cell(line[0]) else None,
                    speed=int(line[1]) if parse_cell(line[1]) else None,
                    odometer=float(line[2]) if parse_cell(line[2]) else None,
                    state_of_charge=int(line[3]) if parse_cell(line[3]) else None,
                    elevation=int(line[4]) if parse_cell(line[4]) else None,
                    shift_state_id=line[5] if parse_cell(line[5]) else None,
                )
                vehicle.datapoints.append(datapoint)

        # add the new vehicle to thedatabase
        session.add(vehicle)
        session.commit()