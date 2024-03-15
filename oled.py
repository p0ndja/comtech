from machine import Pin, SoftI2C
import ssd1306
import time
import dht

humid_sensor = dht.DHT11(Pin(26))

oled_i2c = SoftI2C(scl=Pin(17), sda=Pin(16))
oled_scr = ssd1306.SSD1306_I2C(128,64,oled_i2c)

while True:
    oled_scr.fill(0)
    oled_scr.text(f"====[Member]====",0, 0)
    oled_scr.text('Palapon     1661', 0, 10)
    oled_scr.text('Phattharani 6043', 0, 20)
    
    current_time = time.localtime()
    hours = current_time[3]
    minutes = current_time[4]
    seconds = current_time[5]

    # Format the time string
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    oled_scr.text(f"===[{formatted_time}]===", 0, 30)
    
    humid_sensor.measure()
    temp = humid_sensor.temperature()
    humi = humid_sensor.humidity()
    
    oled_scr.text(f"Temp.:      {temp:3.1f}", 0, 40)
    oled_scr.text(f"Humid:      {humi:3.1f}", 0, 50)

    oled_scr.show()
    time.sleep(1)
    
    
    