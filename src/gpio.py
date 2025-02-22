"""GPIO module for handling button input."""

import RPi.GPIO as GPIO
import time
from config.settings import GPIO_BUTTON_PIN, BUTTON_DEBOUNCE_TIME

class ButtonHandler:
    def __init__(self, callback):
        """Initialize GPIO button handler.
        
        Args:
            callback: Function to call when button is pressed
        """
        self.callback = callback
        self.last_press_time = 0

    def setup(self):
        """Set up GPIO pin for button input."""
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(GPIO_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(
                GPIO_BUTTON_PIN,
                GPIO.FALLING,
                callback=self._button_callback,
                bouncetime=int(BUTTON_DEBOUNCE_TIME * 1000)
            )
            return True
        except Exception as e:
            print(f"GPIO setup error: {str(e)}")
            return False

    def _button_callback(self, channel):
        """Handle button press event with debouncing."""
        current_time = time.time()
        if (current_time - self.last_press_time) >= BUTTON_DEBOUNCE_TIME:
            self.last_press_time = current_time
            self.callback()

    def cleanup(self):
        """Clean up GPIO resources."""
        GPIO.cleanup()
