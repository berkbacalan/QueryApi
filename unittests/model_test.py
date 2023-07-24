import unittest
from datetime import datetime
from unittest.mock import Mock
from src.models import Metric
from sqlalchemy import func


class MetricTestCase(unittest.TestCase):
    def setUp(self):
        self.metric1 = Metric(date=datetime.strptime('2023-07-15', '%Y-%m-%d').date(), channel='adcolony', country='US',
                              os='ios', impressions=100, clicks=10, installs=5, spend=50.0, revenue=100.0)
        self.metric2 = Metric(date=datetime.strptime('2023-07-15', '%Y-%m-%d').date(), channel='google', country='CA',
                              os='Android', impressions=200, clicks=20, installs=10, spend=100.0, revenue=200.0)
        self.metric3 = Metric(date=datetime.strptime('2023-07-15', '%Y-%m-%d').date(), channel='adcolony', country='GB',
                              os='ios', impressions=150, clicks=15, installs=7, spend=75.0, revenue=150.0)

    def test_metric_count(self):
        metrics = [self.metric1, self.metric2, self.metric3]
        mock_db = Mock()
        mock_db.query.return_value.count.return_value = len(metrics)

        count = mock_db.query(Metric).count()
        self.assertEqual(count, len(metrics))

    def test_metric_filter_by_channel(self):
        metrics = [self.metric1, self.metric2, self.metric3]
        mock_db = Mock()
        mock_db.query.return_value.filter.return_value.all.return_value = [metric for metric in metrics if
                                                                           metric.channel == 'adcolony']

        filtered_metrics = mock_db.query(Metric).filter(Metric.channel == 'adcolony').all()
        self.assertEqual(len(filtered_metrics), 2)

    def test_metric_sum_revenue(self):
        metrics = [self.metric1, self.metric2, self.metric3]
        mock_db = Mock()
        mock_db.query.return_value.with_entities.return_value.scalar.return_value = sum(
            metric.revenue for metric in metrics)

        total_revenue = mock_db.query(Metric).with_entities(func.sum(Metric.revenue)).scalar()
        self.assertEqual(total_revenue, sum(metric.revenue for metric in metrics))


if __name__ == '__main__':
    unittest.main()
