from machine import Pin
from time import sleep_ms
import firmware

bootloader_gpio_pin     =   4


bootloader_sw=Pin(bootloader_gpio_pin,Pin.IN,Pin.PULL_UP)
sleep_ms(100)

if bootloader_sw():
    firmware.init()

