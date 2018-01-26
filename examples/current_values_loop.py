"""
Usage example for ADXL355 Python library

This example prints on console (each 0.1 seconds)
the current values of axes on accelerometer
"""

import time
import sys
sys.path.append('../lib/')

from adxl355 import ADXL355  # pylint: disable=wrong-import-position

device = ADXL355()           # pylint: disable=invalid-name

while True:
    axes = device.get_axes() # pylint: disable=invalid-name
    print(axes)
    time.sleep(0.1)
