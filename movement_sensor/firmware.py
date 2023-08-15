from machine import reset, lightsleep
from time import sleep_ms
import sys

from MODULES import HC12,PIR

# configuration variables
sleep_interval_ms   = 1000
hc12_set_pin        = 5
hc12_uart_channel   = 2
battery_adc_pin     = 2
pir_sensor_pin      = 4

rf=HC12(hc12_uart_channel,hc12_set_pin)
rf._socket.init(tx=2)
pir_sensor=PIR(pir_sensor_pin)

# read device id form internal file, if it cant it resets
with open('DEVICE.ID','r') as f:
    DEVICE_ID=f.readline()

# check for request from central
def check_request():
    while True:
        msg=rf.recv_msg()
        if msg is not None:
            try:
                msg=msg.decode()
                if DEVICE_ID in msg:
                    rf.send_msg(encode_status(pir_sensor))
                    sleep_ms(50)
                    break
            except:
                pass


# enconde a msg with the sensor state and batery information
# to send to the alarm central
def encode_status(sensor,battery=None):
    return DEVICE_ID+str(sensor())
    # return DEVICE_ID+str(reed_switch())+str(battery())

"""
The system checks for a request from central every 5 seconds
and send the sensor and battery information and then 
goes to deep sleep for power saving
"""

def init():
    # battery=BATTERY(battery_adc_pin)
    while True:
        try:
            check_request()
            # rf.send_msg(encode_status(pir_sensor))
            sleep_ms(100)
            # rf.send_msg(encode_status(reed_switch,battery))
            lightsleep(sleep_interval_ms)
        except Exception as e:
            sys.print_exception(e)


