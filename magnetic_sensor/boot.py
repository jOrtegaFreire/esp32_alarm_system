import firmware
import sys
from machine import Pin, reset
from time import sleep_ms
from os import remove
from MODULES import HC12

# configuration variables
run_firmware    =   True
run_relp_pin    =   4

run_relp=Pin(run_relp_pin,Pin.IN,Pin.PULL_UP)

try:
    if run_relp():
        firmware.init()
except KeyboardInterrupt:   
    pass
except Exception as e:
    sys.print_exception(e)
