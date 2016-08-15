Usage Examples
==============

To use this library with an Adalogger FeatherWing on Adafruit Feather HUZZAH
with ESP8266, you can use the following code::

    import urtc
    from machine import I2C, Pin
    i2c = I2C(Pin(5), Pin(4)) # The SCL is on GPIO5, the SDA is on GPIO4
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
