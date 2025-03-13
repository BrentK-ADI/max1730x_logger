# MAX1730x Logger
These scripts are intended to provide a cross-platform method for capturing
register data for the Analog Devices MAX1730x series of Fuel Gauge.

This code was tested and developed for the [MAX17303](https://www.analog.com/en/products/max17303.html)
but is portable to other parts in the series.

The output data format from the application is a plain-text CSV file including
all available registers in the device as well as the timestamp of the capture.
All CSV data is in hexadecimal format, with the exception of the timestamp which
is in seconds (Epoch time).

## Operation
The scripts may be run with the following parameters. The default output filename
will be based on the current date and time of the system. The default bus and
iface will be based on the host platform.
```
usage: max1730x_logger.py [-h] [-i IFACE] [-b BUS_NUM] [-o OUT_FILE] [-x] [-t INTERVAL]

Simple application for continuously logging the register map for the MAX1730x series of parts

options:
  -h, --help            show this help message and exit
  -i IFACE, --iface IFACE
                        Select Interface: smbus2,ftdi (default: ftdi)
  -b BUS_NUM, --bus BUS_NUM
                        I2C bus number for the interface. (default: 1)
  -o OUT_FILE, --output OUT_FILE
                        File name for the output CSV (default: max1730x_log_2025-03-13_101227.csv)
  -x                    Exit the application on a bus error. (default: False)
  -t INTERVAL, --time INTERVAL
                        Collection interval, in seconds. (default: 5.0)
```

## Setup & Pre-requisites
### Linux: Raspberry PI
There are several known issues with the Raspberry PI's I2C peripheral when
dealing with SMBus and other devices, with the most notable being the inability
to handle clock stretching correctly.

As of RaspberryPI 4, this issue appears to be resolved in the newly added I2C3
and I2C6 instances.  It is highly recommended to leverage one of these new
peripheral instances if using a Raspberry Pi 4 or higher. To enable I2C-6 on
GPIO 22 and 23, add the following line to the /boot/firmware/config.txt (or
/boot/config.txt) file: `dtoverlay=i2c6,pins_22_23`.

### Windows: EvKit (FTDI)
The MAX1730x EvKit uses a FTDI2322H device.  To maintain functionality with the
EvKit's GUI, the interface implementation of this script uses the ftd2xx Python
package which is a wrapper around the FTDI DLLs.  The resulting command and
control code was derived from the FTDI's MPSSE Library and example projects.

To install ftd2xx, simply run `pip install ftd2xx`

**NOTE:** When working under Windows, the bus number is typically 1




