from machine import Pin, SoftI2C, ADC
import utime as time
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import sys
import random
import time

LEVEL_FACTOR = 3
RANDOM_SEED = 1234
RANDOM_SEED_FACTOR = 0

top = 0

def set_seed(sd:int):
    global RANDOM_SEED
    RANDOM_SEED = sd

def set_level(lv:int):
    global LEVEL_FACTOR
    LEVEL_FACTOR = lv

def gen_equation():
    global LEVEL_FACTOR, RANDOM_SEED, RANDOM_SEED_FACTOR
    # random.seed(RANDOM_SEED + RANDOM_SEED_FACTOR)
    RANDOM_SEED_FACTOR += 1
    if LEVEL_FACTOR == 1:
        eqa = [random.randint(1,20), ["+","+","+","+","+","-","-","-","-","-","*","/"][random.randint(0,11)], random.randint(1,10)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 1):
            return gen_equation()
        return eqa
    elif LEVEL_FACTOR == 2:
        eqa = [random.randint(1,50), ["+","+","+","-","-","-","*","/"][random.randint(0,7)], random.randint(1,50)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 2):
            return gen_equation()
        return eqa
    else:
        eqa = [random.randint(1,99), ["+","+","-","-","*","/"][random.randint(0,5)], random.randint(1,99)]
        if eqa[0] < eqa[2]:
                eqa = [eqa[2],eqa[1],eqa[0]]
        if not check_hard_lv(eqa, 3):
            return gen_equation()
        return eqa

def check_hard_lv(eqa,lv):
    x,o,y = eqa
    if o == "/" and y % x != 0:
        return False

    sum = 0
    if o == "+":
        sum = x+y
    elif o == "-":
        sum = x-y
    elif o == "*":
        sum = x*y
    elif o == "/":
        sum = x/y
    else:
        return False

    if (lv == 1 and sum <= 50) or (lv == 2 and (sum <= 200 and sum >= 20)) or (lv == 3 and (sum <= 999 and sum >= 50)):
        return True
    return False

def answer(eqa):
    x,o,y = eqa
    if o == "+":
        return x+y
    elif o == "-":
        return x-y
    elif o == "*":
        return x*y
    elif o == "/":
        return x/y
    else:
        return None

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

mic_pin = Pin(26, Pin.IN)

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
    global current_str
    lcd.clear()
    print(f"{current_str}")
    if len(current_str) > 32:
        current_str = current_str[-1]
        lcd.clear()
    else:
        lcd.putstr(current_str)

def broadcastMessage(message: str):
    lcd.clear()
    if (len(message) < 16):
        message += "\n\n"
    lcd.putstr(message)

def create_custom_char(char_data, char_position):
    """ Defines a custom character on the LCD.

    Args:
        char_data: Byte array representing the custom character (8x5).
        char_position: Position in the character map (0 to 7).
    """
    # Set character position and function for sending data
    lcd.command(0x40 | (char_position & 0x07))  # Set CGRAM address

    # Send character data byte by byte
    for data in char_data:
        lcd.data(data)

    # Reset to display mode
    
def initialize():
    set_seed(1234)
    set_level(1)
    
    init_custom_char()
    
def init_custom_char():
    lcd.custom_char(0, bytearray([
        0b00000,
        0b01010,
        0b11111,
        0b11111,
        0b01110,
        0b00100,
        0b00000,
        0b00000
    ]))
    lcd.custom_char(1, bytearray([
        0b00000,
        0b01010,
        0b10101,
        0b10001,
        0b01010,
        0b00100,
        0b00000,
        0b00000
    ]))

    #Smile
    lcd.custom_char(2, bytearray([
        0B00000,
        0B10001,
        0B01010,
        0B10001,
        0B00000,
        0B11111,
        0B10101,
        0B01110
    ]))
    #Nerd
    lcd.custom_char(3, bytearray([
        0B00000,
        0B01010,
        0B10101,
        0B01010,
        0B00000,
        0B10001,
        0B01110,
        0B00000
    ]))
    #Dead
    lcd.custom_char(4, bytearray([
        0B00000,
        0B11011,
        0B11011,
        0B00000,
        0B00000,
        0B01010,
        0B00100,
        0B01010
    ]))

mic_pin = Pin(26, Pin.IN)
adc = ADC(mic_pin)
adc.width(ADC.WIDTH_12BIT)  # Set ADC resolution to 12 bits
def get_mic_data():
  """
  Reads the raw analog data from the microphone sensor.

  Returns:
      int: The raw ADC value from the microphone sensor.
  """
  return adc.read()

if __name__ == "__main__":
    initialize()
    mic_commulative = 0
    while True:
        user_answer = ""
        current_char = None
        score = 0
        heart = 3
        # while True:
          #  lcd.putstr(chr(0))
           # lcd.putstr(chr(1))
        current_str = "   Quick Math   Press A to start"
        write_to_screen()
        while True:
            keys = scan_keypad(keypad_i2c,KEYPAD_ADDR)
            if len(keys) == 1 and keys[0] == "A":
                lcd.clear()
                break
        current_str = "Difficulty (1-3)"
        write_to_screen()
        while True:
            keys = scan_keypad(keypad_i2c,KEYPAD_ADDR)
            if len(keys) == 1:
                if (current_char == None) or (current_char != keys[0]):
                    current_char = keys[0]
                    if current_char in ["1","2","3"]:
                        set_level(int(keys[0]))
                        current_str = "Selected "
                        if (keys[0] == "1"):
                            current_str += f"Easy {chr(2)} "
                        elif (keys[0] == "2"):
                            current_str += f"Normal{chr(3)}"
                        else:
                            current_str += f"Hard {chr(4)} "
                        current_str += "A:Start D:Cancel"
                        user_answer = keys[0]
                        lcd.clear()
                        write_to_screen()
                    elif (current_char == "D" and len(user_answer) > 0):
                        lcd.clear()
                        current_str = "Difficulty (1-3)"
                        user_answer = ""
                        write_to_screen()
                        current_char = None
                    elif (user_answer in ["1","2","3"] and current_char == "A"):
                        lcd.clear()
                        user_answer = ""
                        current_char = None
                        current_str = "Game is starting"
                        write_to_screen()
                        break
        for i in range(0,4):
            current_str += "...."
            write_to_screen()
            time.sleep_ms(500)
        lcd.clear()
        while True:
            equation = gen_equation()
            ans = answer(equation)
            print(f"LV: {LEVEL_FACTOR}, SEED: {RANDOM_SEED}, {equation[0]} {equation[1]} {equation[2]} = {ans}")
            eq = f"{equation[0]}{equation[1]}{equation[2]}="
            current_str = eq
            write_to_screen()
            try:
                while True:
                    keys = scan_keypad(keypad_i2c,KEYPAD_ADDR)
                    if len(keys) == 1:
                        if (current_char == None) or (current_char != keys[0]):
                            current_char = keys[0]
                            if (current_char == "A"):
                                if (len(user_answer) > 0):
                                    break
                            elif (current_char == "D" and len(user_answer) > 0):
                                user_answer = user_answer[:-1]
                                current_str = current_str[:-1] + " "
                                write_to_screen()
                                current_str = current_str[:-1]
                            elif (current_char == "C" and len(user_answer) > 0):
                                user_answer = ""
                                current_str = eq
                                write_to_screen()
                            elif (current_char in ["0","1","2","3","4","5","6","7","8","9"]):
                                user_answer += current_char
                                current_str += current_char
                                write_to_screen()
                    elif len(keys) > 1:
                        for i in keys:
                            if current_char != i:
                                current_char = i
                                if (current_char == "A"):
                                    if (len(user_answer) > 0):
                                        break
                                elif (current_char == "D" and len(user_answer) > 0):
                                    user_answer = user_answer[:-1]
                                    current_str = current_str[:-1] + " "
                                    write_to_screen()
                                    current_str = current_str[:-1]
                                elif (current_char == "C" and len(user_answer) > 0):
                                    user_answer = ""
                                    current_str = eq
                                    write_to_screen()
                                elif (current_char in ["0","1","2","3","4","5","6","7","8","9"]):
                                    user_answer += current_char
                                    current_str += current_char
                                    write_to_screen()
                    else:
                        current_char = ""
                        if (len(user_answer) > 0):
                            mic_value = get_mic_data()
                            if mic_value != 4095:
                                # print(mic_value)
                                mic_commulative += mic_value
                        if (mic_commulative >= 1000):
                            mic_commulative = 0
                            break
                    # time.sleep_ms(20-len(current_char))
                # Exit loop when press "A"
                if (user_answer != None and len(user_answer) != 0 and int(user_answer) == ans):
                    score += 1
                    message = ["     Great!     ", "      Good      ", "      Nice      ", "    Awesome!    ", "   Well Done!   ", "    Correct!    "][random.randint(0,5)]
                    msg = message + "      "
                    for i in range(0,heart):
                        msg += chr(0)
                    for i in range(0,3-heart):
                        msg += chr(1)
                    broadcastMessage(msg)
                else:
                    heart -= 1
                    message = ["     Wrong!     ", "      Nope      ", "      Fail      ", "    Incorrect   ", "    Try Again   ", "     Nah D:     "][random.randint(0,5)]
                    if (heart == 0):
                        message = "   Game Over!   "
                    msg = message + "      "
                    for i in range(0,heart):
                        msg += chr(0)
                    for i in range(0,3-heart):
                        msg += chr(1)
                    broadcastMessage(msg)
                    if (heart <= 0):
                        time.sleep_ms(1000)
                        if (score > top):
                            top = score
                        broadcastMessage(f"   Game Over!   Score:{score} Top:{top}")
                        time.sleep_ms(5000)
                        break
                print("Score",score)
                time.sleep_ms(1000)
                lcd.clear()
                user_answer = ""
            except KeyboardInterrupt:
                sys.exit(0)