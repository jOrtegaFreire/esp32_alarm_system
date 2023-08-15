from machine import Pin, reset
from time import sleep_ms
import firmware

bootloader_gpio_pin     =   4
bootloader_sw=Pin(bootloader_gpio_pin,Pin.IN,Pin.PULL_UP)
sleep_ms(1000)

# check if bootloader sw is pressed and run firmware
if bootloader_sw():
    firmware.init()
