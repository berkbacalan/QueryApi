from typing import Any, List
from sqlalchemy.orm.query import Query
from src import models


def apply_group_by_clauses(query: Query[Any] = None, group_by: str = None):
    if group_by:
        group_by_columns = group_by.split(",")
        query = query.group_by(*[getattr(models.Metric, column) for column in group_by_columns])
    return query


def apply_filters(query: Query[Any], filters: List = None):
    if filters:
        return query.filter(*filters)
    return query
