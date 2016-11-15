# -*- coding: utf-8 -*-
"""
Andreas Finkler
10.11.2016

Class to control the ZeroSeg addon.
"""

from ZeroSeg import led

DEVICE_ID = 0

class Display(led.sevensegment):

    def __init__(self):
        super(Display, self).__init__()
        self._DIGITS[u'°'] = 0x63
        self.clear()

    def letter(self, deviceId, position, char, dot=False, redraw=True):
        """
        Looks up the most appropriate character representation for char
        from the digits table, and writes that bitmap value into the buffer
        at the given deviceId / position.

        Overwrites the existing letter function to support unicode strings.
        """
        assert dot in [0, 1, False, True]
        if type(char) is not str and type(char) is not unicode:
            char = str(char)
        value = self._DIGITS.get(char, self._UNDEFINED) | (dot << 7)
        self.set_byte(deviceId, position, value, redraw)


    def write_text(self, deviceId, text):
        """
        Outputs the text (as near as possible) on the specific device. If
        text is larger than 8 characters, then an OverflowError is raised.

        Overwrites the existing write_text function to support unicode strings.
        """
        unicodeText = text.decode('utf-8')
        assert 0 <= deviceId < self._cascaded, "Invalid deviceId: {0}".format(deviceId)
        if len(unicodeText) > 8:
            raise OverflowError('{0} too large for display'.format(text))
        for pos, char in enumerate(unicodeText.ljust(8)[::-1]):
            self.letter(deviceId, led.constants.MAX7219_REG_DIGIT0 + pos, char, redraw=False)
        self.flush()


    def _writeTime(self, dateTimeObject):
        hour = dateTimeObject.hour
        minute = dateTimeObject.minute
        second = dateTimeObject.second
        dot = second % 2 == 0  # calculate blinking dot
        # Set hours
        self.letter(DEVICE_ID, 4, int(hour / 10))  # Tens
        self.letter(DEVICE_ID, 3, hour % 10, dot)  # Ones
        # Set minutes
        self.letter(DEVICE_ID, 2, int(minute / 10))  # Tens
        self.letter(DEVICE_ID, 1, minute % 10)  # Ones


    def _writeDate(self, dateTimeObject):
        day = dateTimeObject.day
        month = dateTimeObject.month
        # set day
        self.letter(DEVICE_ID, 8, int(day/10))
        self.letter(DEVICE_ID, 7, int(day%10), dot=True)
        # set month
        self.letter(DEVICE_ID, 6, int(month/10))
        self.letter(DEVICE_ID, 5, int(month%10), dot=True)


    def writeDateAndTime(self, dateTimeObject):
        self._writeTime(dateTimeObject=dateTimeObject)
        self._writeDate(dateTimeObject=dateTimeObject)


    def writeTime(self, dateTimeObject):
        hour = dateTimeObject.hour
        minute = dateTimeObject.minute
        second = dateTimeObject.second
        # Set hours
        self.letter(DEVICE_ID, 8, int(hour / 10))  # Tens
        self.letter(DEVICE_ID, 7, hour % 10)  # Ones
        # slash
        self.letter(DEVICE_ID, 6, '-')
        # Set minutes
        self.letter(DEVICE_ID, 5, int(minute / 10))  # Tens
        self.letter(DEVICE_ID, 4, minute % 10)  # Ones
        # slash
        self.letter(DEVICE_ID, 3, '-')
        # Set seconds
        self.letter(DEVICE_ID, 2, int(second / 10))  # Tens
        self.letter(DEVICE_ID, 1, second % 10)  # Ones


    def writeDate(self, dateTimeObject):
        day = dateTimeObject.day
        month = dateTimeObject.month
        year = dateTimeObject.year
        # set day
        self.letter(DEVICE_ID, 8, int(day / 10))
        self.letter(DEVICE_ID, 7, int(day % 10), dot=True)
        # set month
        self.letter(DEVICE_ID, 6, int(month / 10))
        self.letter(DEVICE_ID, 5, int(month % 10), dot=True)
        # set year
        self.letter(DEVICE_ID, 4, str(year)[0])
        self.letter(DEVICE_ID, 3, str(year)[1])
        self.letter(DEVICE_ID, 2, str(year)[2])
        self.letter(DEVICE_ID, 1, str(year)[3])


    def writeTemperatureLowHigh(self, tempLow, tempHigh):
        """
        Write the min and max temperature in the format "L-10H+03".
        :param tempLow:     minimum temperature as integer
        :param tempHigh:    maximum temperature as integer
        """
        temperatureString = "L{signLow}{tempLow:02d}H{signHigh}{tempHigh:02d}"
        signLow = '-' if tempLow < 0 else ' '
        signHigh = '-' if tempHigh < 0 else ' '
        self.write_text(DEVICE_ID, temperatureString.format(signLow=signLow, tempLow=abs(tempLow),
                                                            signHigh=signHigh, tempHigh=abs(tempHigh)))


    def writeTemperatureCurrent(self, temp):
        """
        Write the current temperature in the format "Cur -10".
        :param temp:        current temperature as integer
        """
        temperatureString =  "Cur{sign}{temp:02d}°C"
        sign = '-' if temp < 0 else ' '
        self.write_text(DEVICE_ID, temperatureString.format(sign=sign, temp=abs(temp)))