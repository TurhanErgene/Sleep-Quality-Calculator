import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID = 'your_wifi_ssid'  # Replace with your WiFi SSID
WIFI_PASS = 'your_wifi_password'  # Replace with your WiFi password

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "your Adafruit IO username"  # Replace with your Adafruit IO username
AIO_KEY = "your Adafruit IO key"  # Replace with your Adafruit IO key
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_LIGHT_FEED = "T1RU5/feeds/light"
AIO_SLEEP_QUALITY_FEED = "T1RU5/feeds/sleep-quality"
AIO_TEMPERATURE_FEED = "T1RU5/feeds/temperature"
AIO_HUMIDITY_FEED = "T1RU5/feeds/humidity"


