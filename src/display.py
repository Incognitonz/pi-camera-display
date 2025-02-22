"""Display module for handling HDMI output."""

import cv2
import numpy as np
from config.settings import DISPLAY_RESOLUTION

class Display:
    def __init__(self):
        """Initialize the display handler."""
        self.window_name = "Camera Feed"
        self.is_active = True
        cv2.namedWindow(self.window_name, cv2.WINDOW_FULLSCREEN)

    def show_frame(self, frame):
        """Display a frame on the HDMI output."""
        if not self.is_active:
            return

        try:
            if frame is not None:
                # Resize frame if needed
                if frame.shape[:2] != DISPLAY_RESOLUTION:
                    frame = cv2.resize(frame, DISPLAY_RESOLUTION)
                cv2.imshow(self.window_name, frame)
                cv2.waitKey(1)
        except Exception as e:
            print(f"Display error: {str(e)}")

    def blank_screen(self):
        """Display a black screen for screen saver mode."""
        if self.is_active:
            try:
                black_screen = np.zeros((DISPLAY_RESOLUTION[1], DISPLAY_RESOLUTION[0], 3), dtype=np.uint8)
                cv2.imshow(self.window_name, black_screen)
                cv2.waitKey(1)
                self.is_active = False
            except Exception as e:
                print(f"Screen blanking error: {str(e)}")

    def wake_screen(self):
        """Reactivate the display."""
        self.is_active = True

    def cleanup(self):
        """Clean up display resources."""
        cv2.destroyAllWindows()
