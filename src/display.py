"""Display module for handling HDMI output."""

import os
import time
import cv2
import numpy as np
from config.settings import DISPLAY_RESOLUTION

class Display:
    def __init__(self):
        """Initialize the display handler."""
        self.window_name = "Camera Feed"
        self.is_active = True
        
        # Ensure DISPLAY is set
        if not os.environ.get('DISPLAY'):
            os.environ['DISPLAY'] = ':0'
        
        # Wait for X server to be ready
        self._wait_for_x_server()
        
        try:
            # Set up fullscreen window
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        except Exception as e:
            print(f"Failed to create window: {str(e)}")
            print("DISPLAY:", os.environ.get('DISPLAY'))
            print("XAUTHORITY:", os.environ.get('XAUTHORITY'))
            raise

    def _wait_for_x_server(self, timeout=30):
        """Wait for X server to be available."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                cv2.namedWindow("test")
                cv2.destroyWindow("test")
                return True
            except Exception:
                time.sleep(1)
        
        raise RuntimeError("X server not available after timeout")

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
            # Try to recreate window
            try:
                cv2.destroyAllWindows()
                cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            except Exception as e:
                print(f"Failed to recover display: {str(e)}")

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
        try:
            # Ensure window is still available
            cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE)
        except:
            # Recreate window if needed
            try:
                cv2.destroyAllWindows()
                cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
                cv2.setWindowProperty(self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            except Exception as e:
                print(f"Failed to recover display on wake: {str(e)}")

    def cleanup(self):
        """Clean up display resources."""
        try:
            cv2.destroyAllWindows()
        except Exception as e:
            print(f"Cleanup error: {str(e)}")
