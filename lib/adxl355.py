"""ADXL355 Python library for Raspberry PI.

This module implements basic operations for ADXL355
accelerometer chip for Raspberry Pi boards

.. _ADXL355 PMDZ Info:
   https://wiki.analog.com/resources/eval/user-guides/eval-adicup360/hardware/adxl355

"""

import spidev

# ADXL345 constants

# SPI config
SPI_MAX_CLOCK_HZ = 10000000
SPI_MODE = 0b00
SPI_BUS = 0
SPI_DEVICE = 0

#Addresses
XDATA3 = 0x08
XDATA2 = 0x09
XDATA1 = 0x0A
YDATA3 = 0x0B
YDATA2 = 0x0C
YDATA1 = 0x0D
ZDATA3 = 0x0E
ZDATA2 = 0x0F
ZDATA1 = 0x10
RANGE = 0x2C
POWER_CTL = 0x2D

# Data Range
RANGE_2G = 0x01
RANGE_4G = 0x02
RANGE_8G = 0x03

# Values
READ_BIT = 0x01
WRITE_BIT = 0x00
DUMMY_BYTE = 0xAA
MEASURE_MODE = 0x06 # Only accelerometer

class ADXL355:
    """
    Class to interact with ADXL355 device

    Allows user to read, write and obtain data
    from the accelerometer
    """
    def __init__(self, measure_range=RANGE_2G):
        # SPI init
        self.spi = spidev.SpiDev()
        self.spi.open(SPI_BUS, SPI_DEVICE)
        self.spi.max_speed_hz = SPI_MAX_CLOCK_HZ
        self.spi.mode = SPI_MODE

        # Device init
        self._set_measure_range(measure_range)
        self._enable_measure_mode()

    def write_data(self, address, value):
        """Writes data on ADXL355 device address.

        Args:
            address (int): Address to write in ADXL355.
            value (int): Value to write in address.

        Returns:
            None
        """
        device_address = address << 1 | WRITE_BIT
        self.spi.xfer2([device_address, value])

    def read_data(self, address):
        """Reads data from ADXL355 device.

        Args:
            address (int): Address to read from ADXL355.

        Returns:
            int: Value in speficied address in accelerometer
        """
        device_address = address << 1 | READ_BIT
        return self.spi.xfer2([device_address, DUMMY_BYTE])[1]

    def read_multiple_data(self, address_list):
        """Reads multiple data from ADXL355 device.

        Args:
            address_list (list): List of addresses to read from.

        Returns:
            list: Value of each address in accelerometer
        """
        spi_ops = []
        for address in address_list:
            spi_ops.append(address << 1 | READ_BIT)
        spi_ops.append(DUMMY_BYTE)

        return self.spi.xfer2(spi_ops)[1:]

    def _set_measure_range(self, measure_range):
        """Sets measure range on ADXL355 device.

        Args:
            measure_range (int): Measure range to set in ADXL355.

        Returns:
            None
        """
        self.write_data(RANGE, measure_range)

    def _enable_measure_mode(self):
        """
        Enables measure mode on ADXL355 device.

        Returns:
            None
        """
        self.write_data(POWER_CTL, MEASURE_MODE)

    def get_axes(self):
        """
        Gets the current data from the axes.

        Returns:
            dict: Current value for x, y and z axis
        """

        # Reading data
        raw_data = self.read_multiple_data(
            [XDATA1, XDATA2, XDATA3, YDATA1, YDATA2, YDATA3, ZDATA1, ZDATA2, ZDATA3]
        )
        x_data = raw_data[0:3]
        y_data = raw_data[3:6]
        z_data = raw_data[6:9]

        # Join data
        x_data = (x_data[0] >> 4) + (x_data[1] << 4) + (x_data[2] << 12)
        y_data = (y_data[0] >> 4) + (y_data[1] << 4) + (y_data[2] << 12)
        z_data = (z_data[0] >> 4) + (z_data[1] << 4) + (z_data[2] << 12)

        # Apply two complement
        if x_data & 0x80000 == 0x80000:
            x_data = ~x_data + 1

        if y_data & 0x80000 == 0x80000:
            y_data = ~y_data + 1

        if z_data & 0x80000 == 0x80000:
            z_data = ~z_data + 1

        # Return values
        return {'x': x_data, 'y': y_data, 'z': z_data}
