# DI2008-Python

## About
Interface for the DI-2008 in Python.
Version 1.2.0

Python 3.10+

Modified from original interface in Python by DATAQ Instruments under MIT License

Maintainer: Clark Hensley ch3136@msstate.edu

## Getting Started
Install via pip from PyPI:
```sh
pip install di2008-python
```

See Available DI-2008s:
```py
from di2008_python import print_all_daq_metadata
print_all_daq_metadata()
```

Instantiate DI2008 Object with Dictionary of Parameters:
```py
from di2008_python import DI2008, DI2008Channels, DI2008Layout, DI2008TCType

# Enable the DI-2008 with a K-Type thermocopule in Analog Channel 1, an N-Type Thermocouple in Analog Channel 3, and the Digital Channel active
di2008 = DI2008({
        # Global Settings
        DI2008GlobalAnalogLayout: (DI2008Layout.TC, DI2008TCType.K)
        DI2008GlobalScanRateSettings.SRATE: 4,
        DI2008GlobalScanRateSettings.DEC: 1,
        DI2008GlobalScanRateSettings.FILTER: {
            DI2008AllChannels: DI2008FilterModes.AVERAGE,
            },
        # Serial Numbers of DAQs to apply
        DI2008GlobalSerialNums: [<DI-2008 Serial Num>, <DI-2008 Serial Num>, ...],
        # Overwriting settings for a given DI-2008
        <DI-2008 Serial Num>: {
            DI2008Channels.CH1: (DI2008Layout.TC, DI2008TCType.N),
            DI2008GlobalScanRateSettings.FILTER: {
                DI2008Channels.CH1: DI2008FilterModes.LAST_POINT,
                }
            }
```

This interface uses named enumerations to ensure that what settings are being used is clear and concise

## Current Features:
* Thermocouples
* ADC Reading
* Changing Scan Rate, Decimation, and Filtering Mode
* Automatic ChannelStretch Synchronized Initialization
* Enforce cleanup on stopping
* Changing Packet Size
* Interface with the `info` operator

## Planned Features:
* Reading configuration from .json/.toml files as well as raw Python dictionaries
* Digital Channels
* Specify Digital Input as well as Output
* CJCDelta
* Rate Measurement
* LED Color

Further information about the DI-2008 can be found on [DATAQ's website](https://www.dataq.com/products/di-2008) and via the [DI-2008 Protocol](https://www.dataq.com/resources/pdfs/misc/di-2008%20protocol.pdf).
