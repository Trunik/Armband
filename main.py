# using Micropython for this project mostly due to the ability 
# to use both processors in the RP2040. CircuitPython can not
# do that as of this writing, but Version 7 of CircuitPython 
# will be released soon. It might have it.

import from machine UART, SPI, I2C, Pin
import DS3231
import Adafruit_ESP_control
import BME280
import LSM303A

