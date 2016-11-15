"""
Andreas Finkler
08.11.2016
"""

import unittest
from src.weather import Weather


class WeatherTest(unittest.TestCase):

    def test_getCurrentTemperature(self):
        temp = Weather().getCurrentTemperature()
        print temp
        self.assertTrue(hasattr(temp, 'min'))
        self.assertTrue(hasattr(temp, 'max'))
        self.assertTrue(hasattr(temp, 'current'))


    def test_getForecastTemperature(self):
        temp = Weather().getForecastTemperature()
        print temp
        self.assertTrue(hasattr(temp, 'min'))
        self.assertTrue(hasattr(temp, 'max'))


if __name__=='__main__':
    unittest.main()