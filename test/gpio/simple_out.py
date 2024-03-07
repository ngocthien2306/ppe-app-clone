import Jetson.GPIO as GPIO
import time

# Pin Definitions
output_pin = [33,31, 37, 7, 11, 13, 15, 21, 23, 29, 16, 18, 22, 24, 26, 32, 36, 38, 12, 19]  # BCM pin 18, BOARD pin 12

def main():
    # Pin Setup:
    GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.LOW)

    print("Starting demo now! Press CTRL+C to exit")
    curr_value = GPIO.LOW
    try:
        while True:
            time.sleep(0.5)
            # Toggle the output every second
            print("Outputting {} to pin {}".format(curr_value, output_pin))
            GPIO.output(output_pin, curr_value)
            curr_value = not curr_value
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()