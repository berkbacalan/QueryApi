import unittest
from fastapi.testclient import TestClient
from src.main import app
import json


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_get_metrics(self):
        response = self.client.get("http://localhost:8000/get_metrics/?countries=CA&group_by=channel&sort_by=-cpi"
                                   "&select_columns=cpi%2Cspend%2Cchannel")
        response_data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data[0]["cpi"], 2.0748663101604277)
        self.assertEqual(response_data[0]["spend"], 1164)


if __name__ == '__main__':
    unittest.main()
