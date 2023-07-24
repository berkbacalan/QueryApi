from sqlalchemy import Column, Date, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Metric(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    channel = Column(String, index=True)
    country = Column(String, index=True)
    os = Column(String, index=True)
    impressions = Column(Integer)
    clicks = Column(Integer)
    installs = Column(Integer)
    spend = Column(Float)
    revenue = Column(Float)
