import time                   # Allows use of time.sleep() for delays
from mqtt import MQTTClient   # For use of MQTT protocol to talk to Adafruit IO
import keys                   # Contain all keys used here
import wifiConnection         # Contains functions to connect/disconnect from WiFi 
import dht
from machine import ADC, Pin


tempSensor = dht.DHT11(machine.Pin(15))  # DHT11 Constructor
ldr = ADC(Pin(26))
led = Pin("LED", Pin.OUT)

# ADC for LM35 temperature sensor
adc = machine.ADC(27)
sf = 4095 / 65535  # Scale factor
volt_per_adc = 3.3 / 4095

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


def assessSleepQuality(temperature, light, humidity):
    """
    TEMPORARY: Relaxed thresholds for experimental/demo purposes.

    Explanation:
    - The ranges here are intentionally broader to simulate different sleep quality outcomes.
    - In production, these should be tightened based on real user data or scientific standards.

    Recommended Production Ranges:
    - Temperature: 18–24°C
    - Light (darkness %): 90–100% (darker = better)
    - Humidity: 40–60% (somewhat flexible)

    """

    # Fragile mode: easier to get "good" or "average"
    if temperature < 16 or temperature > 28:
        return "poor"
    elif light < 50:  # Higher means darker, so <50 is bright = poor
        return "poor"
    elif humidity < 25 or humidity > 75:
        return "poor"
    elif (18 <= temperature <= 25) and (light >= 70) and (45 <= humidity <= 55):
        return "good"
    else:
        return "average"


def setLEDs(quality):
    redLED.off()
    yellowLED.off()
    greenLED.off()

    if quality == "poor":
        redLED.on()
    elif quality == "average":
        yellowLED.on()
    elif quality == "good":
        greenLED.on()


def calculateSleepQuality():
    temperature = getTemperature()
    light = getLightValue()
    humidity = getHumidity()

    print(
        f"Temperature: {temperature:.2f}°C, Darkness: {light:.2f}%, Humidity: {humidity}%"
    )

    quality = assessSleepQuality(temperature, light, humidity)
    setLEDs(quality)

    print(f"Sleep quality is {quality}")
    
    # Publish to Adafruit IO
    try:
        client.publish(keys.AIO_TEMPERATURE_FEED, str(round(temperature, 2)))
        time.sleep(2)
        client.publish(keys.AIO_HUMIDITY_FEED, str(humidity))
        time.sleep(2)
        client.publish(keys.AIO_LIGHT_FEED, str(round(light, 2)))
        time.sleep(2)
        client.publish(keys.AIO_SLEEP_QUALITY_FEED, quality)
        print("Published data to Adafruit IO")
    except Exception as e:
        print("Failed to publish:", e)



def main():
    while True:
        calculateSleepQuality()
        time.sleep(5)

# WiFi Connection
try:
    ip = wifiConnection.connect()
except KeyboardInterrupt:
    print("WiFi connection interrupted")

# MQTT Setup
client = MQTTClient(
    keys.AIO_CLIENT_ID,
    keys.AIO_SERVER,
    keys.AIO_PORT,
    keys.AIO_USER,
    keys.AIO_KEY
)

client.connect()
print("Connected to Adafruit IO")



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
        client.disconnect()
        wifiConnection.disconnect()
        print("Disconnected from Adafruit IO.")


