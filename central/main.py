from esp32_html import html_index,html_reboot,html_login,html_wifimanager,html_switches,html_camera_switches
from machine import Pin,reset,enable_irq
import json
import sys

# configuration variables
reset_gpio_pin      =   12
armed               =   False
request_timeout_ms  =   1000

# reset pin interrupt
def reset_unit(pin):
    reset()

reset_pin=Pin(reset_gpio_pin,Pin.IN)
reset_pin.irq(trigger=Pin.IRQ_FALLING, handler=reset_unit)



# send html response back to client
def send_response(conn,payload,args=None,after_command=None):
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    if type(payload) is str: conn.sendall(payload)
    else: payload(conn,args)
    conn.close()
    if after_command is not None:
        after_command()

# get html request
def get_request(s):
    conn, addr = s.accept()
    # print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    # print('Content = %s' % request)
    return conn,addr,request

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:

        conn,addr,request=get_request(s)

        # PAGES
        reboot=request.find('/reboot')

        # HANDLERS 
        if users==6:pass
        elif switches==6 or switches==7:
            _post=request.find('POST')
            if _post==2:
                for _switch in switches_gpio:
                    if request.find(_switch.replace(' ','+')) and request[request.find(_switch.replace(' ','+'))+len(_switch)]=='=':
                        switches_gpio[_switch](not switches_gpio[_switch]())
            send_response(conn,html_switches,args=switches_gpio)
        elif camera_switches==6 or camera_switches==7:
            _post=request.find('POST')
            if _post==2:
                for _switch in camera_switches_gpio:
                    if request.find(_switch.replace(' ','+')) and request[request.find(_switch.replace(' ','+'))+len(_switch)]=='=':
                        camera_switches_gpio[_switch](not camera_switches_gpio[_switch]())
            send_response(conn,html_camera_switches,args=camera_switches_gpio)
        elif wifimanager==6:
            send_response(conn,html_wifimanager,args=wm)
        elif save_wifi==7:
            ssid,password=get_ssid(request) 
            print(ssid)
            print(password)
        elif reboot==6:send_response(conn,html_reboot(),after_command=reset)
        elif logout==6:
            logged=False
            send_response(conn,html_login())
        else:send_response(conn,html_index)

except Exception as e:
    sys.print_exception(e)
    reset()