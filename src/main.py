from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .helpers import apply_filters, apply_group_by_clauses
from src.database import get_db, load_initial_data
from src import models, database
from .utils import create_filters, create_query_columns, format_results, sort_results

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)


def initialize_app():
    load_initial_data()


initialize_app()


@app.on_event("startup")
def startup():
    database.get_db()


@app.on_event("shutdown")
def shutdown():
    database.disconnect()


@app.get("/")
def read_root():
    return {"Server is running with status": "200"}


@app.get("/get_metrics/")
def get_metrics(
        date_from: str = None,
        date_to: str = None,
        channels: str = None,
        countries: str = None,
        operating_systems: str = None,
        group_by: str = None,
        sort_by: str = None,
        select_columns: str = None,
        db: Session = Depends(get_db)
):
    filters = create_filters(date_from=date_from, date_to=date_to, channels=channels, countries=countries,
                             operating_systems=operating_systems)

    query_columns = create_query_columns(select_columns, group_by)

    query = db.query(*query_columns)

    query = apply_filters(query, filters)

    query = apply_group_by_clauses(query, group_by)

    results = query.all()

    formatted_results = format_results(results, query_columns)
    sorted_results = sort_results(formatted_results, sort_by)

    return sorted_results
