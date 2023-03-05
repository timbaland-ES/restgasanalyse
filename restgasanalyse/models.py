from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurements'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    value = Column(Integer)