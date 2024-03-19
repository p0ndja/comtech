from machine import Pin, SoftI2C
import utime as time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import sys

current_str = ""
end_time = time.time() + 60 # 60 second
# KEYS = [
#    ['1','2','3','A'],
#    ['4','5','6','B'],
#    ['7','8','9','C'],
#    ['*','0','#','D'] ]
keypad_i2c = SoftI2C(scl=Pin(16), sda=Pin(4), freq=100000)
KEYPAD_ADDR = 0x20

LCD_I2C_ADDR = 0x27
lcd_i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32
lcd = I2cLcd(lcd_i2c, LCD_I2C_ADDR, 2, 16)

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
            # print("R{}='{:>04s}'".format(row+1,bin(x)[2:]))
            keys.append(key)
    return keys

def caltime(second):
    minute = 0
    if (second >= 60):
        minute = second // 60
        second = second % 60
    if (second < 0):
        return f"TIME UP!"
    return f"{minute:02d}:{second:02d}"

def write_to_screen():
    cal = caltime(end_time - time.time())
    global current_str        
    print(f"{cal}\n{current_str}\n")
    if len(current_str) >= 16:
        current_str = current_str[-1]
        lcd.clear()
    lcd.putstr(f"{cal}\n{current_str}\n")
    if "TIME UP!" in cal:
        sys.exit(0)
if __name__ == "__main__":
    # Use GPIO22=SCL, GPIO21=SDA
    current_str = "A"
    try:
        current_char = ""
        while True:
            keys = scan_keypad(keypad_i2c,KEYPAD_ADDR)
            if len(keys) == 1:
                if (current_char == None) or (current_char != keys[0]):
                    current_char = keys[0]
                    current_str += current_char
                    print(current_char)
            elif len(keys) > 1:
                for i in keys:
                    if current_char != i:
                        current_char = i
                        current_str += current_char
                        print(current_char)
                        break
            else:
                current_char = ""
            write_to_screen()
            # time.sleep_ms(20-len(current_char))
    except KeyboardInterrupt:
        pass
    finally:
        print('Done')
