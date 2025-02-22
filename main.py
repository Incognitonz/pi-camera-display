"""Main entry point for the camera display application."""

import signal
import sys
import time
from src.camera import Camera
from src.display import Display
from src.gpio import ButtonHandler
from src.screensaver import ScreenSaver

def handle_exit(signum, frame):
    """Handle clean exit on system signals."""
    print("\nShutting down...")
    cleanup()
    sys.exit(0)

def cleanup():
    """Clean up system resources."""
    camera.cleanup()
    display.cleanup()
    button_handler.cleanup()

def handle_button_press():
    """Handle button press events."""
    screen_saver.reset_timer()

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    # Initialize components
    camera = Camera()
    display = Display()
    screen_saver = ScreenSaver(
        blank_callback=display.blank_screen,
        wake_callback=display.wake_screen
    )
    button_handler = ButtonHandler(callback=handle_button_press)

    # Set up components
    if not camera.setup():
        print("Failed to initialize camera")
        sys.exit(1)

    if not button_handler.setup():
        print("Failed to initialize GPIO")
        sys.exit(1)

    # Start camera
    if not camera.start():
        print("Failed to start camera")
        sys.exit(1)

    print("Camera display system running...")

    # Main loop
    try:
        while True:
            # Get and display frame
            frame = camera.get_frame()
            display.show_frame(frame)
            
            # Update screen saver
            screen_saver.update()
            
            # Small sleep to prevent CPU overload
            time.sleep(0.01)

    except Exception as e:
        print(f"Runtime error: {str(e)}")
        cleanup()
        sys.exit(1)
