"""Screen saver module for managing display timeout."""

import time
from config.settings import SCREEN_SAVER_TIMEOUT

class ScreenSaver:
    def __init__(self, blank_callback, wake_callback):
        """Initialize screen saver.
        
        Args:
            blank_callback: Function to call when screen should blank
            wake_callback: Function to call when screen should wake
        """
        self.blank_callback = blank_callback
        self.wake_callback = wake_callback
        self.last_activity_time = time.time()
        self.is_active = False

    def reset_timer(self):
        """Reset the screen saver timer and wake the display."""
        self.last_activity_time = time.time()
        if self.is_active:
            self.is_active = False
            self.wake_callback()

    def update(self):
        """Check if screen saver should be activated."""
        if not self.is_active:
            current_time = time.time()
            if (current_time - self.last_activity_time) >= SCREEN_SAVER_TIMEOUT:
                self.is_active = True
                self.blank_callback()
