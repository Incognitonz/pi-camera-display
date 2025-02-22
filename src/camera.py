"""Camera module for handling Raspberry Pi Camera Module 2."""

from picamera2 import Picamera2
from config.settings import CAMERA_RESOLUTION, CAMERA_FRAMERATE

class Camera:
    def __init__(self):
        """Initialize the camera with specified settings."""
        self.camera = None
        self.running = False

    def setup(self):
        """Set up the camera with configured settings."""
        try:
            self.camera = Picamera2()
            config = self.camera.create_video_configuration(
                main={"size": CAMERA_RESOLUTION, "format": "RGB888"},
                controls={"FrameRate": CAMERA_FRAMERATE}
            )
            self.camera.configure(config)
            return True
        except Exception as e:
            print(f"Camera setup error: {str(e)}")
            return False

    def start(self):
        """Start the camera capture."""
        if self.camera and not self.running:
            try:
                self.camera.start()
                self.running = True
                return True
            except Exception as e:
                print(f"Camera start error: {str(e)}")
                return False
        return False

    def stop(self):
        """Stop the camera capture."""
        if self.camera and self.running:
            try:
                self.camera.stop()
                self.running = False
                return True
            except Exception as e:
                print(f"Camera stop error: {str(e)}")
                return False
        return False

    def get_frame(self):
        """Capture and return a single frame."""
        if self.camera and self.running:
            try:
                return self.camera.capture_array()
            except Exception as e:
                print(f"Frame capture error: {str(e)}")
                return None
        return None

    def cleanup(self):
        """Clean up camera resources."""
        if self.camera:
            self.stop()
            self.camera.close()
