from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint, Table, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from server.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, default="")
    __table_args__ = (UniqueConstraint("name"),)

    # Relationships
    datapoints = relationship("DataPoint", back_populates="vehicle")

class ShiftStates(Base):
    __tablename__ = "shift_states"

    id = Column(String(1), primary_key=True, index=True)
    name = Column(String, default="")
    __table_args__ = (UniqueConstraint("name"),)

class DataPoint(Base):
    __tablename__ = "datapoints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vehicle_id = Column(String, ForeignKey("vehicles.id"))

    timestamp = Column(DateTime, nullable=False)
    speed = Column(Integer)
    odometer = Column(Float)
    state_of_charge = Column(Integer)
    elevation = Column(Integer)
    shift_state_id = Column(String, ForeignKey("shift_states.id"))

    #relationships
    shift_state = relationship("ShiftStates", lazy="joined")
    vehicle = relationship("Vehicle", back_populates="datapoints")

