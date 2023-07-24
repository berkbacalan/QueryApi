import csv
from datetime import datetime

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./application.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def disconnect(db: Session = Depends(get_db)):
    db.close()


def load_initial_data():
    db = SessionLocal()

    if db.query(models.Metric).count() > 0:
        db.close()
        return

    import os
    csv_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset.csv")

    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            date = datetime.strptime(row["date"], '%Y-%m-%d').date()
            channel = row["channel"]
            country = row["country"]
            os = row["os"]
            impressions = int(row["impressions"])
            clicks = int(row["clicks"])
            installs = int(row["installs"])
            spend = float(row["spend"])
            revenue = float(row["revenue"])

            metric = models.Metric(
                date=date,
                channel=channel,
                country=country,
                os=os,
                impressions=impressions,
                clicks=clicks,
                installs=installs,
                spend=spend,
                revenue=revenue
            )
            db.add(metric)

    db.commit()
    db.close()
