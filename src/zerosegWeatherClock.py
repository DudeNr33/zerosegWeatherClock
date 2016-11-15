"""
07.11.2016
Andreas Finkler
Main module to run the raspiClock.
"""

# change this later
import sys
sys.path.append('/home/pi/programming/raspiClock')

import threading
import time
from datetime import datetime
import RPi.GPIO as GPIO

from src.weather import Weather
from src.display import Display

DEFAULT_UPDATE_INTERVAL = 0.1           # delay in seconds between view updates
DEFAULT_VIEW_DISPLAY_TIME = 5.0         # time to display a view in seconds before it switches back to the default view

# Constants defining the views
VIEW_TOTAL_NUMBER = 4                   # total amount of available views
VIEW_INDEX_TIME = 0
VIEW_INDEX_DATE = 1
VIEW_INDEX_TEMPERATURE_FORECAST = 2
VIEW_INDEX_TEMPERATURE_CURRENT = 3

# Constants for GPIO pins
SWITCH_1 = 17
SWITCH_2 = 26

class ZerosegWeatherClock(object):

    def __init__(self):
        self.timer = None
        self.viewIndex = 0          # defines which info will be displayed
        self.weather = Weather()
        self.display = Display()
        self._setupButtons()


    def _setupButtons(self):
        GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbers
        GPIO.setup(SWITCH_1, GPIO.IN)
        GPIO.setup(SWITCH_2, GPIO.IN)


    def _resetViewIndex(self):
        """
        Reset the viewIndex to 0 ( = time and date) and the timer to None.
        """
        self.timer = None
        self.viewIndex = 0
        self.display.clear()
        self.updateView()  # call the updateView method directly so the changes are displayed immediately.


    def _incrementViewIndex(self):
        """
        Increment the viewIndex to switch to the next view.
        """
        if self.timer is not None:
            self.timer.cancel()
        self.viewIndex += 1
        self.viewIndex = self.viewIndex % VIEW_TOTAL_NUMBER      # overflow
        self.timer = threading.Timer(DEFAULT_VIEW_DISPLAY_TIME, self._resetViewIndex)
        self.timer.start()
        self.display.clear()
        self.updateView()       # call the updateView method directly so the changes are displayed immediately.


    def _updateDateTime(self):
        self.display.writeDateAndTime(datetime.now())


    def _updateTime(self):
        self.display.writeTime(dateTimeObject=datetime.now())


    def _updateDate(self):
        self.display.writeDate(dateTimeObject=datetime.now())


    def _updateTemperatureForecast(self):
        temperature = self.weather.getForecastTemperature()
        self.display.writeTemperatureLowHigh(tempLow=temperature.min, tempHigh=temperature.max)


    def _updateCurrentTemperature(self):
        temperature = self.weather.getCurrentTemperature()
        self.display.writeTemperatureCurrent(temp=temperature.current)


    def updateView(self):
        """
        Update the current view.
        """
        # check the viewIndex and call the corresponding function
        if self.viewIndex == VIEW_INDEX_TIME:
            self._updateTime()
        elif self.viewIndex == VIEW_INDEX_DATE:
            self._updateDate()
        elif self.viewIndex == VIEW_INDEX_TEMPERATURE_FORECAST:
            self._updateTemperatureForecast()
        elif self.viewIndex == VIEW_INDEX_TEMPERATURE_CURRENT:
            self._updateCurrentTemperature()


    def main(self):
        while True:
            try:
                if not GPIO.input(SWITCH_1) or not GPIO.input(SWITCH_2):
                    self._incrementViewIndex()
                self.updateView()
                time.sleep(DEFAULT_UPDATE_INTERVAL)
            except KeyboardInterrupt:
                # self._incrementViewIndex()
                # continue
                self.display.clear()
                raise


if __name__=='__main__':
    ZerosegWeatherClock().main()

