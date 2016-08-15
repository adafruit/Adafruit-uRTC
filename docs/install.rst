Installation
************

In order to install this library, you need to copy the ``urtc.py`` file onto
your board, so that it can be imported.


ESP8266 Port, Binary Releases
=============================

The easiest way to make this library importable with the binary releases of
MicroPython for ESP8266 is to upload the ``urtc.py`` file to the board using
the WebREPL utility.


ESP8266 Port, Compiled Firmware
===============================

If you are compiling your own firmware, the easiest way to include this library
in it is to copy or symlink the ``urtc.py`` file to the ``esp8266/scripts``
directory before compilation.


Other Ports
===========

For boards that are visible as USB mass storage after connecting to your
computer, simply copy the ``urtc.py`` file onto that storage.
