import unittest
from datetime import datetime
import pytz
from kabu_json_lib.datetime_utils import fetch_now


class TestDatetimeUtils(unittest.TestCase):
    def test_fetch_now(self):
        now = fetch_now()
        self.assertIsInstance(now, datetime)
        self.assertEqual(str(now.tzinfo), str(pytz.timezone("Asia/Tokyo")))


if __name__ == "__main__":
    unittest.main()
