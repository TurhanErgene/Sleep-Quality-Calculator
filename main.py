import dht
from machine import ADC, Pin
import time


tempSensor = dht.DHT11(machine.Pin(15))     # DHT11 Constructor 
ldr = ADC(Pin(26))
led = Pin("LED", Pin.OUT)

# ADC for LM35 temperature sensor
adc = machine.ADC(27)
sf = 4095/65535 # Scale factor
volt_per_adc = (3.3 / 4095)

# Define the GPIO pins for the LEDs
yellowLED = Pin(17, Pin.OUT)
greenLED = Pin(16, Pin.OUT)
redLED = Pin(18, Pin.OUT)


# gets the temperature value from the LM35 sensor
# returns the temperature value in Celsius
def getTemperature():
    time.sleep(2)
    millivolts = adc.read_u16()

    adc_12b = millivolts * sf
    volt = adc_12b * volt_per_adc

    dx = abs(50 - 0)
    dy = abs(0 - 0.5)
    shift = volt - 0.5
    temp = shift / (dy / dx)
    
    return temp

# gets the light value from the LDR sensor
# returns the darkness value in percentage
def getLightValue():
    light = ldr.read_u16()
    darkness = round(light / 65535 * 100, 2)
    
    return darkness

# gets the humidity value from the DHT11 sensor
def getHumidity():
    try:
        tempSensor.measure()
        humidity = tempSensor.humidity()
        return humidity
    except Exception as error:
       print("Exception occurred", error)
    time.sleep(2)
    

# calculates the sleep quality based on the temperature, light, and humidity values
# turns on the red LED if the sleep quality is poor, yellow LED if average, and green LED if good
def calculateSleepQuality():
    # temperature = tempSensor.temperature() # Uncomment if using DHT11 for temperature

    temperature = getTemperature()
    light = getLightValue() 
    humidity = getHumidity()
    print("Temperature: {}°C, Light: {}%, Humidity: {}%".format(temperature, light, humidity))

    if temperature < 18 or temperature > 24 or light > 50 or humidity < 30 or humidity > 70:
        redLED.on()
        yellowLED.off()
        greenLED.off()
        print("Sleep quality is poor")
    elif (18 <= temperature <= 24) and (light <= 50) and (30 <= humidity <= 70):
        yellowLED.on()
        redLED.off()
        greenLED.off()
        print("Sleep quality is average")
    else:
        greenLED.on()
        redLED.off()
        yellowLED.off()
        print("Sleep quality is good")
    

def main():
    while True:
        calculateSleepQuality()
        time.sleep(5)

# Run the main function
if __name__ == "__main__":
    led.on()  # Turn on the onboard LED to indicate the program is running
    print("Starting sleep quality monitoring...")  
    try:
        main()
    except KeyboardInterrupt:
        print("Program stopped by user.")
    finally:
        led.off()  # Turn off the onboard LED when exiting
    main()
