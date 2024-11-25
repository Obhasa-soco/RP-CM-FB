from firestore_helper import FirebaseDB
from barcode_reader import BarcodeReader
import RPi.GPIO as GPIO
import time
import os

# Setup GPIO
OUTPUT_PIN = 17  # Define the GPIO pin number for the output
GREEN_PIN = 18    # Green LED
RED_PIN = 23      # Red LED
YELLOW_PIN = 24   # Yellow LED

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setup(OUTPUT_PIN, GPIO.OUT)  # Set the output pin as an output
GPIO.output(OUTPUT_PIN, GPIO.LOW)  # Set output pin low
GPIO.setup(GREEN_PIN, GPIO.OUT)  # Set up green LED
GPIO.setup(RED_PIN, GPIO.OUT)    # Set up red LED
GPIO.setup(YELLOW_PIN, GPIO.OUT) # Set up yellow LED

def check_internet():
    """Function to check internet connectivity by pinging Google's DNS."""
    return os.system("ping -c 1 8.8.8.8") == 0

def update_leds(internet_status):
    """Update LED states based on internet connectivity."""
    if internet_status:
        GPIO.output(GREEN_PIN, GPIO.HIGH)  # Connected
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
        return 'connected'
    else:
        GPIO.output(RED_PIN, GPIO.HIGH)     # Not connected
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        return 'not connected'


def relay_port(barcode_status):
    # If barcode status indicates success, blink the OUTPUT_PIN LED
    if barcode_status:
        GPIO.output(OUTPUT_PIN, GPIO.HIGH)  # Set OUTPUT_PIN high
        time.sleep(0.1)  # Wait for 0.1 seconds
        GPIO.output(OUTPUT_PIN, GPIO.LOW)   # Set OUTPUT_PIN low

if __name__ == '__main__':
    firebase_db = FirebaseDB()  # Create an instance of the FirebaseDB class
    barcode_reader = BarcodeReader()  # Create an instance of the BarcodeReader class

    try:
        while True:
            # Periodic internet check
            internet_status = check_internet()
            connection = update_leds(internet_status)

            if connection == 'connected':
                # Read barcode
                barcode = barcode_reader.read_barcode()  
                # Find and delete the barcode status from the database
                status = firebase_db.find_and_delete_by_id('barcode_status', barcode)
                relay_port(status)
                print(status)

            # Delay for smoother operation
            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        # Turn off all LEDs and clean up GPIO on exit
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(YELLOW_PIN, GPIO.LOW)
        GPIO.output(OUTPUT_PIN, GPIO.LOW)  # Set output pin low
        GPIO.cleanup()
