from typing import Any, List, Optional
from src import models
from sqlalchemy import func


def create_filters(
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        channels: Optional[str] = None,
        countries: Optional[str] = None,
        operating_systems: Optional[str] = None
) -> List:
    filters = []
    try:
        if date_from:
            filters.append(models.Metric.date >= date_from)
        if date_to:
            filters.append(models.Metric.date < date_to)
        if channels:
            filters.append(models.Metric.channel.in_(channels.split(",")))
        if countries:
            filters.append(models.Metric.country.in_(countries.split(",")))
        if operating_systems:
            filters.append(models.Metric.os.in_(operating_systems.split(",")))
    except Exception as e:
        print("ERROR during create_filters: ", str(e))
    return filters


def create_query_columns(select_columns: str = None, group_by: str = None) -> List:
    query_columns = []
    try:
        if select_columns:
            select_statements = select_columns.split(",")

            for ss in select_statements:
                if ss == 'cpi':
                    query_columns.append(
                        (func.sum(models.Metric.spend) / func.sum(models.Metric.installs)).label("cpi"))
                elif ss not in group_by:
                    query_columns.append(func.sum(getattr(models.Metric, ss)).label(ss))
                else:
                    query_columns.append(getattr(models.Metric, ss))
    except Exception as e:
        print("ERROR during create_query_columns: ", str(e))
    return query_columns


def sort_results(formatted_results: List, sort_by: str = None):
    if not sort_by:
        return formatted_results
    try:
        sorted_formatted_results = []
        sort_by_columns = sort_by.split(",")
        for column in sort_by_columns:
            if column.startswith("-"):
                sorted_formatted_results = sorted(formatted_results, key=lambda x: x[column[1:]], reverse=True)
            else:
                sorted_formatted_results = sorted(formatted_results, key=lambda x: x[column])
        return sorted_formatted_results
    except Exception as e:
        print("ERROR during sort_results: ", str(e))
        return format_results


def format_results(results: List[Any] = None, query_columns: List = None):
    try:
        formatted_results = []
        for row in results:
            formatted_row = {}
            for column in query_columns:
                formatted_row[column.name] = getattr(row, column.name)
            formatted_results.append(formatted_row)
        return formatted_results
    except Exception as e:
        print("ERROR during format results: ", str(e))
