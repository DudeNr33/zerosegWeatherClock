"""
08.11.2016
Andreas Finkler

Uses OpenWeatherMap API
"""

import requests
import datetime
from collections import namedtuple


API_KEY = "28eda2be64ee0ee6fb7b4852a6f57b9d"
CITY_NAME = "Nuremberg"
MODE = "json"
REQUEST_URI_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
REQUEST_URI_FORECAST = "http://api.openweathermap.org/data/2.5/forecast/daily"

# Dictionary keys for current temperature
CURRENT_MAIN_SECTION_KEY = 'main'
CURRENT_TEMPERATURE_MAX_KEY = 'temp_max'
CURRENT_TEMPERATURE_MIN_KEY = 'temp_min'
CURRENT_TEMPERATURE_CURRENT_KEY = 'temp'

# Dictionary keys for forecast temperature
FORECAST_TEMPERATURE_MAX_KEY = 'max'
FORECAST_TEMPERATURE_MIN_KEY = 'min'


class Weather(object):

    def __init__(self):
        self.cachedForecastResponse = None
        self.datetimeOfLastForecastRequest = None
        self.cachedCurrentResponse = None
        self.datetimeOfLastCurrentRequest = None


    def _kelvinToCelsius(self, tempKelvin):
        return int(round(tempKelvin - 273.15))


    def _executeForecastRequest(self):
        """
        Execute the request only if at least 5 minutes have passed to avoid using up all of our API calls.
        :return:
        """
        if self.cachedForecastResponse is None \
                or (datetime.datetime.now() - self.datetimeOfLastForecastRequest).total_seconds() > 300:
            request = requests.get(url=REQUEST_URI_FORECAST, params=dict(q=CITY_NAME, mode=MODE, appid=API_KEY))
            infoDict = request.json()
            self.cachedForecastResponse = infoDict
            self.datetimeOfLastForecastRequest = datetime.datetime.now()
        return self.cachedForecastResponse


    def _executeCurrentRequest(self):
        """
        Execute the request only if at least 5 minutes have passed to avoid using up all of our API calls.
        :return:
        """
        if self.cachedCurrentResponse is None \
                or (datetime.datetime.now() - self.datetimeOfLastCurrentRequest).total_seconds() > 300:
            request = requests.get(url=REQUEST_URI_CURRENT, params=dict(q=CITY_NAME, mode=MODE, appid=API_KEY))
            infoDict = request.json()
            self.cachedCurrentResponse = infoDict
            self.datetimeOfLastCurrentRequest = datetime.datetime.now()
        return self.cachedCurrentResponse


    def getCurrentTemperature(self):
        """
        Get the temperature (min, max, current) in degree celsius.
        :return:
        namedtuple object with attributes min, max, current
        """
        infoDict = self._executeCurrentRequest()
        mainInfo = infoDict.get(CURRENT_MAIN_SECTION_KEY)
        Temperature = namedtuple(typename='Temperature', field_names=['min','max','current'])
        min = self._kelvinToCelsius(mainInfo.get(CURRENT_TEMPERATURE_MIN_KEY))
        max = self._kelvinToCelsius(mainInfo.get(CURRENT_TEMPERATURE_MAX_KEY))
        current = self._kelvinToCelsius(mainInfo.get(CURRENT_TEMPERATURE_CURRENT_KEY))
        return Temperature(min=min, max=max, current=current)


    def getForecastTemperature(self):
        """
        Get the temperature (min, max) in degree celsius
        :return:
        namedtuple object with attributes min, max
        """
        infoDict = self._executeForecastRequest()
        mainInfo = infoDict.get('list')[0]['temp']          # get the entry for today
        Temperature = namedtuple(typename='Temperature', field_names=['min', 'max'])
        min = self._kelvinToCelsius(mainInfo.get(FORECAST_TEMPERATURE_MIN_KEY))
        max = self._kelvinToCelsius(mainInfo.get(FORECAST_TEMPERATURE_MAX_KEY))
        return Temperature(min=min, max=max)