from machine import Pin
from time import sleep

relay1 = Pin(12, Pin.OUT)
relay2 = Pin(13, Pin.OUT)
relay3 = Pin(14, Pin.OUT)
relay4 = Pin(15, Pin.OUT)

relay_list = [relay1, relay2, relay3, relay4]

def on_relay(pin):
    pin.value(1)

def off_relay(pin):
    pin.value(0)

if __name__ == '__main__':
    for i in range(0,len(relay_list)):
        off_relay(relay_list[i])
    slp = 1
    lop = 4
    while lop != 0:
        for i in range(0,len(relay_list)):
            on_relay(relay_list[i])
            sleep(slp)
            off_relay(relay_list[i])
            sleep(slp)
        slp = slp/2
        lop = lop - 1
