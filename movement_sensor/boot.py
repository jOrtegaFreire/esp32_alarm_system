from machine import Pin, reset
from time import sleep_ms
from os import remove
import sys

from MODULES import HC12
import firmware

# configuration variables
bootloader_gpio_pin     =   4
bootloader_sw=Pin(bootloader_gpio_pin,Pin.IN,Pin.PULL_UP)
sleep_ms(1000)

try:
    if bootloader_sw():
        firmware.init()
except KeyboardInterrupt:   
    pass
except Exception as e:
    sys.print_exception(e)
