import unittest
from restgasanalyse.main import mock_sensor_data, Measurement

class TestMock(unittest.TestCase):
    def test_mock_data(self):
        data = mock_sensor_data()
        self.assertIsInstance(data, Measurement)
        self.assertEqual(data.id, 10)
        self.assertLessEqual(data.value, 23)
        self.assertGreaterEqual(data.value, 1)