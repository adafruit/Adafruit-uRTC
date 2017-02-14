Usage Examples
==============

To use this library with an Adalogger FeatherWing on Adafruit Feather HUZZAH
with ESP8266, you can use the following code::

    import urtc
    from machine import I2C, Pin
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    rtc = urtc.PCF8523(i2c)

now you can set the current time::

    datetime = urtc.datetime_tuple(year=2016, month=8, day=14)
    rtc.datetime(datetime)

or read it::

    datetime = rtc.datetime()
    print(datetime.year)
    print(datetime.month)
    print(datetime.day)
    print(datetime.weekday)
