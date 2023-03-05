import unittest
from main import mock_sensor_data

class TestABC(unittest.TestCase):
    def test_mock_data(self):
        data = mock_sensor_data()
