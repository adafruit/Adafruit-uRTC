try:
    import ucollections
    import utime
except ImportError:
    import collections as ucollections
    import time as utime


DateTimeTuple = ucollections.namedtuple("DateTimeTuple",
    "year,month,day,weekday,hour,minute,second,millisecond")


def datetime_tuple(year, month, day, weekday=0, hour=0, minute=0,
                   second=0, millisecond=0):
    """Factory function for DateTimeTuple."""
    return DateTimeTuple(year, month, day, weekday, hour, minute,
                         second, millisecond)


def bcd2bin(value):
    """Convert from the BCD format to binary."""
    return value - 6 * (value >> 4)


def bin2bcd(value):
    """Convert from binary to BCD format."""
    return value + 6 * (value // 10)


def mktime(datetime):
    """Convert ``DateTimeTuple`` to seconds since Jan 1, 2000."""
    return utime.mktime((datetime.year, datetime.month, datetime.day,
        datetime.hour, datetime.minute, datetime.second, datetime.weekday, 0))


class BaseRTC:
    def __init__(self, i2c, address=0x68):
        self.i2c = i2c
        self.address = address

    def _register(self, register, buffer=None):
        """Get or set the value of a register."""
        if buffer is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]
        self.i2c.writeto_mem(self.address, register, buffer)

    def datetime(self, datetime=None):
        """
        Get or set the current date and time.

        The ``datetime`` is a tuple in the form: ``(year, month, day,
        weekday, hour, minute, second, millisecond)``. If not specified,
        the method returns current date and time in the same format.
        """
        buffer = bytearray(7)
        if datetime is None:
            self.i2c.redfrom_mem_into(self, self._DATETIME_REGISTER, buffer)
            return datetime_tuple(
                year=bcd2bin(buffer[6]) + 2000,
                month=bcd2bin(buffer[5]),
                day=bcd2bin(buffer[4]),
                weekday=bcd2bin(buffer[3]),
                hour=bcd2bin(buffer[2]),
                minute=bcd2bin(buffer[1]),
                second=bcd2bin(buffer[0]),
            )
        datetime = datetime_tuple(*datetime)
        buffer[0] = bin2bcd(datetime.second)
        buffer[1] = bin2bcd(datetime.minute)
        buffer[2] = bin2bcd(datetime.hour)
        buffer[3] = bin2bcd(datetime.weekday)
        buffer[4] = bin2bcd(datetime.day)
        buffer[5] = bin2bcd(datetime.month)
        buffer[6] = bin2bcd(datetime.year - 2000)
        self._register(self._DATETIME_REGISTER, buffer)


class DS1307(BaseRTC):
    _NVRAM_REGISTER = 0x08
    _DATETIME_REGISTER = 0x00
    _SQUARE_WAVE_REGISTER = 0x07

    def is_running(self):
        """Return ``True`` if and only if the clock is running."""
        return bool(self._register(0x00) & 0b10000000)

    def pin_frequency(self, value=None):
        """
        Get or set the square wave pin frequency in hertz. Set to -1 to
        switch the pin off. Available values: 0, 1, 4000, 8000 and 32000 Hz.
        """
        if value is None:
            return {
                0x00: 0,
                0x80: -1,
                0x10: 1,
                0x11: 4000,
                0x12: 8000,
                0x13: 32000,
            }[self._register(self._SQUARE_WAVE_REGISTER) & 0x93]
        try:
            buffer = bytearray(({
                0: 0x00,
                -1: 0x80,
                1: 0x10,
                4000: 0x11,
                8000: 0x12,
                32000: 0x13,
            }[value],))
        except KeyError:
            raise ValueError("only 0, 1Hz, 4kHz, 8kHz and 32kHz are supported")
        self._register(self._SQUARE_WAVE_REGISTER, buffer)

    def memory(self, address, buffer=None):
        """Read or write the non-volatile random access memory."""
        return self._register(self._NVRAM_REGISTER + address, buffer)


class DS3231(BaseRTC):
    _STATUS_REGISTER = 0x0f
    _DATETIME_REGISTER = 0x00
    _SQUARE_WAVE_REGISTER = 0x0e

    def lost_power(self):
        """Return ``True`` if the clock lost power and needs to be set."""
        return bool(self._register(self._STATUS_REGISTER) & 0b10000000)

    def datetime(self, datetime):
        if datetime is not None:
            self._register(self._STATUS_REGISTER,
                self._register(self._STATUS_REGISTER) & 0b01111111)
        return super().datetime(datetime)

    def pin_frequency(self, value=None):
        """
        Get or set the square wave pin frequency. Available values are:
        1, 1000, 4000 and 8000 Hz. 0 switches it off.
        """
        if value is None:
            return {
                0x01: 0,
                0x00: 1,
                0x08: 1000,
                0x10: 4000,
                0x18: 8000,
            }[self._register(self._SQUARE_WAVE_REGISTER) & 0x93]
        try:
            buffer = bytearray(({
                0: 0x01,
                1: 0x00,
                1000: 0x08,
                4000: 0x10,
                8000: 0x18,
            }[value],))
        except KeyError:
            raise ValueError("only 1Hz, 1kHz, 4kHz and 8kHz are supported")
        self._register(self._SQUARE_WAVE_REGISTER, buffer)


class PCF8523(BaseRTC):
    _CONTROL3_REGISTER = 0x02
    _DATETIME_REGISTER = 0x03
    _SQUARE_WAVE_REGISTER = 0x0f

    def is_initialized(self):
        return self._register(self._CONTROL3_REGISTER) & 0xE0 != 0xE0

    def datetime(self, datetime):
        if datetime is not None:
            self._register(self._CONTROL3_REGISTER, 0x00) # battery switchover
        return super().datetime(datetime)

    def pin_frequency(self, value=None):
        """
        Get or set the square wave pin frequency. Available values are:
        1, 32, 1000, 4000, 8000, 16000 and 32000 Hz. 0 switches it off.
        """
        if value is None:
            return {
                7: 0,
                6: 1,
                5: 32,
                4: 1000,
                3: 4000,
                2: 8000,
                1: 16000,
                0: 32000,
            }[(self._register(self._SQUARE_WAVE_REGISTER) >> 3) & 0x07]
        try:
            buffer = bytearray(({
                0: 7,
                1: 6,
                32: 5,
                1000: 4,
                4000: 3,
                8000: 2,
                16000: 1,
                32000: 0,
            }[value << 3],))
        except KeyError:
            raise ValueError("only 1Hz, 32Hz, 1kHz, 4kHz, 8kHz, 16kHz "
                             "and 32kHz are supported")
        self._register(self._SQUARE_WAVE_REGISTER, buffer)

