"""
Usage example for ADXL355 Python library

This example prints on console the current values
of axes on accelerometer
"""

import sys
sys.path.append('../lib/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name
axes = device.get_axes()     # pylint: disable=invalid-name
print(axes)
