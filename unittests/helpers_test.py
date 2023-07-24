import unittest
from datetime import datetime
from sqlalchemy.orm.query import Query
from sqlalchemy import and_
from src import models
from src.helpers import apply_filters


class HelperFunctionsTestCase(unittest.TestCase):
    def setUp(self):
        self.metric_query = Query(models.Metric)
        self.filters = [
            models.Metric.date >= datetime.strptime('2023-07-15', '%Y-%m-%d').date(),
            models.Metric.channel == 'adcolony',
            models.Metric.country.in_(['US', 'CA']),
        ]
        self.group_by = 'channel,country'

    def test_apply_filters(self):
        query = apply_filters(self.metric_query, self.filters)
        applied_filters = query.whereclause
        expected_filters = and_(models.Metric.date >= datetime.strptime('2023-07-15', '%Y-%m-%d').date(),
                                models.Metric.channel == 'adcolony',
                                models.Metric.country.in_(['US', 'CA']))
        self.assertEqual(str(applied_filters), str(expected_filters))


if __name__ == '__main__':
    unittest.main()
