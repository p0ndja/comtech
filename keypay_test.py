from machine import Pin, SoftI2C
import utime as time
# KEYS = [
#    ['1','2','3','A'],
#    ['4','5','6','B'],
#    ['7','8','9','C'],
#    ['*','0','#','D'] ]
KEYS = [
    ['D','C','B','A'],
    ['#','9','6','3'],
    ['0','8','5','2'],
    ['*','7','4','1'] ]

COLUMN_BITS = [0b01111111,0b10111111,0b11011111,0b11101111]
def scan_keypad(i2c, addr):
    buf = bytearray(1)
    keys = []
    for row in range(4): # scan each row
        # write one byte to PCF8574 (for row scanning)
        buf[0] = COLUMN_BITS[ row ]
        i2c.writeto(addr, buf)
        # read one byte from PCF8574
        x = i2c.readfrom(addr,1)[0] & 0xf
        if (~x & 0xf) not in [1,2,4,8]:
            # no keypress or multiple keypress
            continue
        col = -1
        # check the i-th column for key press
        for i in range(4): 
            # the key at this column is pressed
            if (x>>i) & 1 == 0:
                col = (3-i) # save column index
                break
        if col >= 0:
            # lookup the key at (row,column)
            key = KEYS[row][col]
            # show active row and input bits
            print("R{}='{:>04s}'".format(row+1,bin(x)[2:]))
            keys.append(key)
    return keys
# Use GPIO22=SCL, GPIO21=SDA
i2c = SoftI2C(freq=100000, scl=Pin(16), sda=Pin(4))
addr = 0x20
try:
    while True:
        keys = scan_keypad(i2c,addr)
        if len(keys) >= 1:
            print(keys)
        time.sleep_ms(100)       
except KeyboardInterrupt:
    pass
finally:
    print('Done')