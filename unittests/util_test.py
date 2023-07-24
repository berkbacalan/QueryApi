from sqlalchemy.orm.query import Query
from src.helpers import apply_filters
from src import models
from datetime import datetime


def test_apply_filters():
    query = Query(models.Metric)

    filters = [
        models.Metric.date >= datetime.strptime('2023-07-15', '%Y-%m-%d').date(),
        models.Metric.channel == 'adcolony',
        models.Metric.country.in_(['US', 'CA'])
    ]

    query = apply_filters(query, filters)

    applied_filters = query.whereclause
    expected_filters = (
            (models.Metric.date >= datetime.strptime('2023-07-15', '%Y-%m-%d').date()) &
            (models.Metric.channel == 'adcolony') &
            (models.Metric.country.in_(['US', 'CA']))
    )
    assert str(applied_filters) == str(expected_filters)
