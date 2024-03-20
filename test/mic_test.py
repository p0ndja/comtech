import micropython
from machine import Pin, ADC
import utime as time

# Define microphone pin
mic_pin = Pin(26, Pin.IN)

# Configure ADC for microphone pin
adc = ADC(mic_pin)
adc.width(ADC.WIDTH_12BIT)  # Set ADC resolution to 12 bits

def get_mic_data():
  """
  Reads the raw analog data from the microphone sensor.

  Returns:
      int: The raw ADC value from the microphone sensor.
  """
  return adc.read()

# Example usage
commulative = 0
while True:
  # Read microphone data
  mic_value = get_mic_data()
  # Print the raw ADC value (0 - 4095)
  if mic_value != 4095:
    # print(mic_value)
    commulative += 1
    print("Mic Trigger")
  else:
    if commulative > 0:
      commulative = 0
      print("Mic Reset")
      
  if (commulative >= 3):
    print("Next")
    commulative = 0
  
  time.sleep_ms(10)

  # You can process the microphone data here,
  # for example, convert it to voltage or perform audio analysis.
  # ...