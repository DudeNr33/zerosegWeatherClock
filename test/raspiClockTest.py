"""
11.07.2016
Andreas Finkler
Unittests for main module.
"""

import unittest
import time
from src import zerosegWeatherClock


class RaspiClockTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_incrementAndResetCounter(self):
        rpiClock = zerosegWeatherClock.ZerosegWeatherClock()
        for i in range(zerosegWeatherClock.VIEW_TOTAL_NUMBER-1):
            rpiClock._incrementViewIndex()
        self.assertEqual(rpiClock.viewIndex, zerosegWeatherClock.VIEW_TOTAL_NUMBER - 1)
        rpiClock._incrementViewIndex()
        self.assertEqual(rpiClock.viewIndex, 0)
        rpiClock._incrementViewIndex()
        self.assertEqual(rpiClock.viewIndex, 1)
        time.sleep(zerosegWeatherClock.DEFAULT_VIEW_DISPLAY_TIME + 1)
        self.assertEqual(rpiClock.viewIndex, 0)


if __name__=='__main__':
    unittest.main()