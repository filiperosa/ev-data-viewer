from db_utils.connect_db import session, engine

from server.models import ShiftState, Vehicle, DataPoint
import server.models as models


# Create tables

models.Base.metadata.create_all(bind=engine)

# Create shift states

park = ShiftState(id="P", name="Park")
drive = ShiftState(id="D", name="Drive")
reverse = ShiftState(id="R", name="Reverse")

session.add_all([park, drive, reverse])
session.commit()