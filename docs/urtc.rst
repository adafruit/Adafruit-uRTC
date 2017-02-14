``urtc`` module
***************

.. module:: urtc

DS1307
======

.. class:: DS1307(i2c, address=0x68)

    .. method:: datetime(datetime)

        Get or set the current time.

        The ``datetime`` is an 8-tuple of the format
        ``(year, month, day, weekday, hour, minute, second, millisecond)``
        describing the time to be set. If not specified, the method returns
        a tuple in the same format.


    .. method:: memory(address, buffer=None)

        Read or write the non-volatile random acces memory.

    .. method:: stop(value=None)

        Get or set the status of the stop clock flag. This can be used to start
        the clock at a precise moment in time.


DS3231
======

.. class:: DS3231(i2c, address=0x68)

    .. method:: datetime(datetime)

        Get or set the current time.

        The ``datetime`` is an 8-tuple of the format
        ``(year, month, day, weekday, hour, minute, second, millisecond)``
        describing the time to be set. If not specified, the method returns
        a tuple in the same format.

    .. method:: alarm_time(self, datetime=None, alarm=0)

        Get or set the alarm time.

        The ``datetime`` is a tuple in the same format as for ``datetime()``
        method.

        The ``alarm`` is the id of the alarm, it can be either 0 or 1.

        For alarm 1, only ``day``, ``hour``, ``minute`` and ``weekday`` values
        are used, the rest is ignored. Alarm 0 additionally supports seconds.
        If a value is ``None``, it will also be ignored.  When the values match
        the current date and time, the alarm will be triggered.

    .. method:: lost_power()

        Return ``True`` if the clock lost the power recently and needs to be
        re-set.

    .. method:: alarm(value=None, alarm=0)

        Get or set the value of the alarm flag. This is set to ``True`` when
        an alarm is triggered, and has to be cleared manually.

    .. method:: stop(value=None)

        Get or set the status of the stop clock flag. This can be used to start
        the clock at a precise moment in time.

PCF8523
=======

.. class:: PCF8523(i2c, address=0x68)

    .. method:: datetime(datetime)

        Get or set the current time.

        The ``datetime`` is an 8-tuple of the format
        ``(year, month, day, weekday, hour, minute, second, millisecond)``
        describing the time to be set. If not specified, the method returns
        a tuple in the same format.

    .. method:: alarm_time(self, datetime=None)

        Get or set the alarm time.

        The ``datetime`` is a tuple in the same format as for ``datetime()``
        method.

        Only ``day``, ``hour``, ``minute`` and ``weekday`` values are used,
        the rest is ignored. If a value is ``None``, it will also be ignored.
        When the values match the current date and time, the alarm will be
        triggered.

    .. method:: lost_power()

        Return ``True`` if the clock lost the power recently and needs to be
        re-set.

    .. method:: alarm(value=None)

        Get or set the value of the alarm flag. This is set to ``True`` when
        an alarm is triggered, and has to be cleared manually.

    .. method:: stop(value=None)

        Get or set the status of the stop clock flag. This can be used to start
        the clock at a precise moment in time.

    .. method:: reset()

        Perform a software reset of the clock module.

    .. method:: battery_low()

        Return ``True`` if the battery is discharged and needs to be replaced.


Utilities
=========

.. class:: DateTimeTuple

    A ``NamedTuple`` of the format required by the ``datetime`` methods.

.. function:: datetime_tuple(year, month, day, weekday, hour, minute, second, millisecond)

    A factory function for :class:`DateTimeTuple`.

.. function:: tuple2seconds(datetime)

    Convert ``datetime`` tuple into seconds since Jan 1, 2000.

.. function:: seconds2tuple

    Convert seconds since Jan 1, 2000 into a :class:`DateTimeTuple`.
