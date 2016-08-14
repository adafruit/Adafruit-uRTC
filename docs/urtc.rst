
.. module:: urtc


Common Functionality
********************

All RTC modules will let you to get or set the current time.

.. autoclass:: BaseRTC
    :members:

Real-time Clock Modules
***********************

Depending on the module, there are some additional functions available.

.. autoclass:: DS1307
    :members:
.. autoclass:: DS3231
    :members:
.. autoclass:: PCF8523
    :members:

Utilities
*********

.. autofunction:: datetime_tuple
.. autofunction:: tuple2seconds
.. autofunction:: seconds2tuple
