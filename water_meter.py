from pubsub import pub
from RPi import GPIO as GPIO

from constants import GPIO_PIN, BOUNCE_TIME


class WaterMeter:
    """This class handles tracking water meter events and status"""
    def __init__(self):
        """Set up the water meter object"""
        self.setup_gpio()

    def __del__(self):
        """Clean up the GPIO object"""
        GPIO.cleanup()  # Clean up

    def setup_gpio(self):
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
        # Set pin 10 to be an input pin and set initial value to be pulled low (off)
        GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Setup event on pin 10 trigger on both rising and falling
        GPIO.add_event_detect(GPIO_PIN, GPIO.BOTH, callback=self.gpio_callback, bouncetime=BOUNCE_TIME)

    @staticmethod
    def gpio_callback(channel):
        if not GPIO.input(GPIO_PIN):
            return
        pub.sendMessage('meter_event')
