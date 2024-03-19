import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep

LCD_I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16

lcd_i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32

lcd = I2cLcd(lcd_i2c, LCD_I2C_ADDR, totalRows, totalColumns)

def caltime(second):
    minute = 0
    if (second >= 60):
        minute = second // 60
        second = second % 60
    return f"{minute:02d}:{second:02d}"
timer = 60
while timer >= 0:
    lcd.putstr(f"{caltime(timer)}\n0 + 0 = \n")
    timer -= 1
    sleep(0.75)
lcd.putstr("Time Up!")