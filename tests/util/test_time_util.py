# To run all tests: 
# python3 -m unittest tests.util.test_time_util
#
# To run a single test:
# python3 -m unittest tests.util.test_time_util.TimeUtilTests.format_stopwatch_seconds

import unittest
from src.util import time_util

class TimeUtilTests(unittest.TestCase):

    def format_stopwatch_seconds(self):
        total_seconds = 5
        expected = "00:00:05"
        actual = time_util.format_stopwatch(total_seconds)
        self.assertEqual(expected, actual)

    def format_stopwatch_minutes(self):
        total_seconds = 5 + 12*60;
        expected = "00:12:05"
        actual = time_util.format_stopwatch(total_seconds)
        self.assertEqual(expected, actual)

    def format_stopwatch_hours(self):
        total_seconds = 5 + 12*60 + 3*60*60;
        expected = "03:12:05"
        actual = time_util.format_stopwatch(total_seconds)
        self.assertEqual(expected, actual)
   
    def format_stopwatch_days(self):
        total_seconds = 5 + 12*60 + 3*60*60 + 47*24*60*60
        expected = "47.03:12:05"
        actual = time_util.format_stopwatch(total_seconds)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()