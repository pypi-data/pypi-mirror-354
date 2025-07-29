import unittest
from kabu_json_lib.bp import bp


class TestBp(unittest.TestCase):
    def test_bp(self):
        self.assertEqual(bp(0.05), 500)
        self.assertEqual(bp(0.01), 100)
        self.assertEqual(bp(0), 0)
        self.assertIsNone(bp(None))


if __name__ == "__main__":
    unittest.main()
