from distutils.core import setup


setup(
    name='urtc',
    py_modules=['urtc'],
    version="1.0",
    description="Drivers for RTC modules for MicroPython.",
    long_description="""\
This library lets you communicate with several real-time clock modules. At
the moment DS1307, DS3231 and PCF8523 are supported.""",
    author='Radomir Dopieralski',
    author_email='micropython@sheep.art.pl',
    classifiers = [
        'Development Status :: 6 - Mature',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
