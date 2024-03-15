from machine import Pin, SoftI2C
import ssd1306

oled_i2c = SoftI2C(scl=Pin(17), sda=Pin(16))
oled_scr = ssd1306.SSD1306_I2C(128,64,oled_i2c)
oled_scr.fill(0)