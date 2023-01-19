from server import models
from server.models import ShiftState, Vehicle, DataPoint
from server.database import engine

from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker

from datetime import datetime

session = sessionmaker()(bind=engine)
