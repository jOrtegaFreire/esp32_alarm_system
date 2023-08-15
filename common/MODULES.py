from machine import UART, Pin, ADC
from time import sleep_us

class HC12:
    """
    433 MHz Transceiver, it uses UART protocol
    and a gpio pin for a configuration mode using
    AT commands
    """        
    
    def __init__(self,channel,ht12_set):
        self.mode=Pin(ht12_set,Pin.OUT)
        self._socket=UART(channel,9600)
        self.mode.on()

    # put module on configuration mode
    def set_mode(self,mode):
        self.mode.on() if mode else self.mode.off()
    
    # send a string msg
    def send_msg(self,msg):
        self._socket.write(msg)
    
    # read a string msg from buffer
    def recv_msg(self):
        return self._socket.read()

class REED_SWITCH:

    """
    Standar Reed switch (NO)
    """

    def __init__(self,gpio_pin,init_state=True):
        self.gpio_pin=Pin(gpio_pin,Pin.IN,Pin.PULL_UP)

    # return switch state
    def __call__(self):
        return self.gpio_pin()
    
class BATTERY:

    """
    Uses internal adc for battery level reading.
    Low and full values need to be calculated depending on
    the values of the resistor network used and type of battery
    """

    def __init__(self,gpio_pin,low_value=1240,full_value=1370):
        adc=ADC(Pin(gpio_pin), atten=ADC.ATTN_6DB)
        self.low_value=low_value
        self.full_value=full_value
    
    def __call__(self):
        return self.level()

    # set low battery value
    def set_low_value(self,low_value):
        self.low_value=low_value

    # set full charge battery value
    def set_full_value(self,full_value):
        self.full_value=full_value

    # read adc value and calculate battery %
    def level(self):
        val=self.adc.read_uv()//1e3
        val=((val-self.low_value)*100)//(self.full_value-self.low_value)
        return val
    
class PIR:

    def __init__(self,gpio_pin):
        self.gpio_pin=Pin(gpio_pin,Pin.IN,Pin.PULL_UP)

    def __call__(self):
        return self.gpio_pin()

class SIREN:

    def __init__(self,gpio_pin):
        self.gpio_pin=Pin(gpio_pin,Pin.OUT,value=0)

    def __call__(self,value):
        self.gpio_pin(value)