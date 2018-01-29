# ADXL355 on Raspberry Pi

Python 3 library to connect ADXL355 PMDZ accelerometer on Raspberry Pi.

Using SPI protocol, the library connects to device to read, write and obtain data from ADXL355.

## Usage

To test this library on Python console:

```
$ python3 -i lib/adxl355.py
```
Then

```python
adxl355 = ADXL355()
axes = adxl355.get_axes()
print(axes)
```

## Settings

All the device values are stored as constants on `lib/adxl355.py` file. The most important are:

* `SPI_BUS`: SPI bus where the accelerometer is connected
* `SPI_DEVICE`: SPI id of the accelerometer

If everything is connected as the 'Wiring' section says, both device values should be `0`.

## Methods

* `constructor(measure_range)`: Initializes an `ADXL355` object. A measure range can be specified as follows: `0x01` for 2G (default), `0x02` for 4G and `0x03` for 8G
* `write_data(address, value)`: Writes `value` to `address`
* `read_data(address)`: Reads ADXL355's `address`
* `read_multiple_data(address_list)`: Reads multiples addresses from ADXL355
* `get_axes()`: Obtains current values for X, Y,Z

# How does it work?

## Requirements

* Raspberry Pi 
  * Tested on Raspberry Pi Zero W
  * Raspbian Stretch Lite installed
* ADXL355 PMDZ
  * More info: [here](https://wiki.analog.com/resources/eval/user-guides/eval-adicup360/hardware/adxl355)

## Enable SPI interface

In order to use SPI on Raspberry Pi, the interface must be enabled. On the raspberry console:

```
$ raspi-config
```

On the menu, select `Interfacing Options/SPI`, and then enable interface.

## Wiring ADXL355 to Raspberry Pi

| ADXL355 Pin Numer  | ADXL Pin description       | GPIO Pin      |
| -----------------: |----------------------------|---------------|
| 1                  | Chip Select                | 24            |
| 2                  | Master Out Slave In (MOSI) | 19            |
| 3                  | Master In Slave Out (MISO) | 21            |
| 4                  | Serial Clock (SCLK)        | 23            |
| 5                  | Digital Ground             | 25            |
| 6                  | Digital Power              | 17            |
| 7                  | Interrupt 1                | Not Connected |
| 8                  | Not Connected              | Not Connected |
| 9                  | Interrupt 2                | Not Connected |
| 10                 | Data Ready                 | Not Connected |
| 11                 | Digital Ground             | 09            |
| 12                 | Digital Power              | 01            |

## Install SPI Python library

To install `spidev`, on Raspberry Pi console:

```
$ sudo apt-get install python3-pip
$ pip3 install spidev
```

## Test device

Two examples are included on this repo.

### Example 1: Obtain current values of axes

To run this example (on Raspberry Pi console):

```
$ cd examples/
$ python3 current_axes_values.py
```

The output should be something like this:

```
{'x': 495873, 'y': 422842, 'z': 67185}
```

### Example 2: Obtain current values of axes each 0.1 secs.

To run this example (on Raspberry Pi console):

```
$ cd examples/
$ python3 current_values_loop.py
```

The output should be something like this:

```
{'x': 487683, 'y': 705456, 'z': 330437}
{'x': 495886, 'y': 799674, 'z': 199731}
{'x': 438536, 'y': 881595, 'z': 462199}
{'x': 614660, 'y': 541619, 'z': 919630}
{'x': 647432, 'y': 857012, 'z': 396566}
{'x': 405775, 'y': 222158, 'z': 66401}
{'x': 495884, 'y': 197575, 'z': 787212}
{'x': 422147, 'y': 807862, 'z': 3152}
...
```