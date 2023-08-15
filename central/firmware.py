from time import ticks_ms,sleep_ms
from machine import Pin,PWM
from math import ceil
import socket
import json
import sys

from wifi_manager import WifiManager
from MODULES import HC12
import html_pages
import images
import OTA

# configuration variables
alarm_running           =   False
alarm_armed             =   True
alarm_gpio_pin          =   2
sensor_timeout_ms       =   2600
http_request_timeout    =   0.2
device_retray_requests  =   3
device_retray_delay_ms  =   10
device_ping_delay_ms    =   150
max_device_retries      =   5

#debug variables
max_ticks_dif           =   0
max_retries             =   0

# rf transceiver and wifi manager
rf=HC12(2,5)
wm=WifiManager()

# retray connection to network
while True:
    if wm.is_connected():
        break
    wm.connect()
    sleep_ms(5000)

# open socket on port 80 with 500ms timout to avoid blocking
# on client connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(http_request_timeout)
s.bind(('', 80))
s.listen(5)

# alarm dummy (for testing)
alarm=PWM(Pin(alarm_gpio_pin),freq=1,duty=0)

# device (sensors) list
devices={
    'pgaXuv':{
        'type':'magnetic_sensor',
        'location':'Recepcion',
        'state':0,
        'battery':75,
        'retry':0
    },
    'DaUnKB':{
        'type':'movement_sensor',
        'location':'Pasillo',
        'state':0,
        'battery':50,
        'retry':0
    }
}
sirens={
    'kaGPjb':{
        'type':'siren',
        'location':'Entrada',
        'battery':60
    }
}

def start_alarm():
    global alarm_running
    if alarm_armed:
        for device in devices:
            if devices[device]['state']:
                alarm_running=True
                for siren in sirens:
                    rf.send_msg(siren+'1')
                    sleep_ms(50)
                alarm.duty(512)

def stop_alarm():
    global alarm_running
    alarm_running=False
    for siren in sirens:
        rf.send_msg(siren+'0')
        sleep_ms(50)
    alarm.duty(0)

def request_devices_information():
    global max_retries
    for device in devices:
        rf.send_msg(device)
        sleep_ms(device_ping_delay_ms)
        response=rf.recv_msg()
        if response is not None:
            try:
                response=response.decode()
                print(f'response.decode():{response}')
                print(f'device_request:{device}')
                if device in response:
                    devices[device]['state']=int(response[-1])
                    print(f"retries until response: {devices[device]['retry']}, response:{response[-1]}")
                    print(f'max_retries: {max_retries}')
                    devices[device]['retry']=0
            except Exception as e:
                sys.print_exception(e)
        else:
            retries=devices[device]['retry']+1
            devices[device]['retry']=retries
            # devices[device]['retry']=devices[device]['retry']+1
            if retries>max_device_retries:
                devices[device]['state']=1
            if retries>max_retries:max_retries=retries

# get a client request
def get_request(_socket):
    try:
        conn, addr = _socket.accept()
        request = conn.recv(1024)
        request=request.decode()
        boundary=OTA.extract_boundary(request)
        if boundary:
            while True:
                if request[-(len(boundary)+4):]==boundary+'--\r\n':
                    _r=None
                    break
                else:
                    _r=conn.recv(1024)
                    _r=_r.decode()
                    request+=_r
        # print('Content = %s' % request)
        return conn,addr,request
    except Exception as e:
        # sys.print_exception(e)
        return None,None,None

# send http/text response to client
def send_text_response(conn,response):
    conn.send('HTTP/1.1 200 OK\r\n')
    conn.send('Content-Type: text/html\r\n')
    conn.send(response)

# send http/image response to client
def send_image_response(con,response):
    pass

# handle requests from clients
def handle_request(conn,request):
    pass

# application main loop
def init():
    global alarm_armed
    # init_sensor_timeout()
    while True:
        # process_sensor_msg()
        # check_sensor_timeout()
        request_devices_information()
        start_alarm()
        conn,addr,request=get_request(s)
        if conn is not None:
            # handle_request(conn,request)
            if "POST /OTA HTTP/1.1" in request:
                OTA.write_file(conn,OTA.extract_filename(request),OTA.extract_file_content(request))
            elif "GET / HTTP/1.1" in request:
                send_text_response(conn,html_pages.html_index(alarm_armed,alarm_running,devices))
            elif "GET /stop HTTP/1.1" in request:
                alarm_armed=False
                stop_alarm()
                send_text_response(conn,html_pages.html_index(alarm_armed,alarm_running,devices))
            elif "GET /start HTTP/1.1" in request:
                alarm_armed=True
                send_text_response(conn,html_pages.html_index(alarm_armed,alarm_running,devices))
            elif "GET /armed.png HTTP/1.1" in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: image/png\r\n')
                conn.send('\r\n')
                conn.send(images.armed_img)
            elif "GET /disarmed.png HTTP/1.1" in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: image/png\r\n')
                conn.send('\r\n')
                conn.send(images.disarmed_img)
            elif "GET /reload.png HTTP/1.1" in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: image/png\r\n')
                conn.send('\r\n')
                conn.send(images.reload_img)
            elif "GET /start.png HTTP/1.1" in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: image/png\r\n')
                conn.send('\r\n')
                conn.send(images.start_img)
            elif "GET /stop.png HTTP/1.1" in request:
                conn.send('HTTP/1.1 200 OK\r\n')
                conn.send('Content-Type: image/png\r\n')
                conn.send('\r\n')
                conn.send(images.stop_img)
            conn.close()