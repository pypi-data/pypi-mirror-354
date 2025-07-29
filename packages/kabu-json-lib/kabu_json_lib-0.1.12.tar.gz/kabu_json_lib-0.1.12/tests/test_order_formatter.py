import unittest
from datetime import datetime
from kabu_json_lib.order_formatter import order_to_one_line


class TestOrderFormatter(unittest.TestCase):
    def test_order_to_one_line(self):
        # テストケース1: 基本的な注文情報
        test_order1 = {
            "long_or_short": "Long",
            "entry_or_exit": "Entry",
            "symbol": "1321",
            "price": 45000,
            "quantity": 16,
            "value": "720,000",
            "order_type": "指値",
            "datetime_obj": datetime(2024, 3, 22, 10, 30, 0)
        }
        expected1 = "[Long -Entry] 1321 @ 45000 *    16 (¥  720,000) [指値] 2024-03-22 10:30:00"
        self.assertEqual(order_to_one_line(test_order1), expected1)

        # テストケース2: 空売り注文
        test_order2 = {
            "long_or_short": "Short",
            "entry_or_exit": "Entry",
            "symbol": "9984",
            "price": 15000,
            "quantity": 100,
            "value": "1,500,000",
            "order_type": "成行",
            "datetime_obj": datetime(2024, 3, 22, 13, 45, 30)
        }
        expected2 = "[Short-Entry] 9984 @ 15000 *   100 (¥1,500,000) [成行] 2024-03-22 13:45:30"
        self.assertEqual(order_to_one_line(test_order2), expected2)

        # テストケース3: 決済注文
        test_order3 = {
            "long_or_short": "Long",
            "entry_or_exit": "Exit",
            "symbol": "9432",
            "price": 8000,
            "quantity": 200,
            "value": "1,600,000",
            "order_type": "IOC指値",
            "datetime_obj": datetime(2024, 3, 22, 15, 0, 0)
        }
        expected3 = "[Long -Exit ] 9432 @  8000 *   200 (¥1,600,000) [IOC指値] 2024-03-22 15:00:00"
        self.assertEqual(order_to_one_line(test_order3), expected3)


if __name__ == "__main__":
    unittest.main()
