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

    def square_wave_pin_mode(self, value=None):
        """Get or set the square wave pin mode."""
        if value is None:
            return self._register(self._SQUARE_WAVE_REGISTER) & 0x93
        self._register(self._SQUARE_WAVE_REGISTER, bytearray((value,)))

    def memory(self, address, buffer=None):
        """Read or write the non-volatile random access memory."""
        return self._register(self._NVRAM_REGISTER + address, buffer)


class DS3231(BaseRTC):
    _STATUS_REGISTER = 0x0f
    _DATETIME_REGISTER = 0x00
    _SQUARE_WAVE_REGISTER = 0x0e

    def lost_power(self):
        return bool(self._register(self._STATUS_REGISTER) & 0b10000000)

    def datetime(self, datetime):
        if datetime is not None:
            self._register(self._STATUS_REGISTER,
                self._register(self._STATUS_REGISTER) & 0b01111111)
        return super().datetime(datetime)

    def square_wave_pin_mode(self, value=None):
        """Get or set the square wave pin mode."""
        if value is None:
            return self._register(self._SQUARE_WAVE_REGISTER) & 0x93
        self._register(self._SQUARE_WAVE_REGISTER, bytearray((value,)))


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

    def square_wave_pin_mode(self, value=None):
        """Get or set the square wave pin mode."""
        if value is None:
            return (self._register(self._SQUARE_WAVE_REGISTER) >> 3) & 0x07
        self._register(self._SQUARE_WAVE_REGISTER, bytearray((value << 3,)))

