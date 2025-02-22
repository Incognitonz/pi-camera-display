# Raspberry Pi Camera Display System

This application displays the Raspberry Pi Camera Module 2 feed on HDMI output with screen saver functionality.

## Features

- Real-time camera feed display via HDMI
- Screen saver (black screen) after 2 minutes of inactivity
- GPIO button to wake display
- Automatic startup on boot
- Clean shutdown handling

## Hardware Requirements

- Raspberry Pi 3 B+
- Raspberry Pi Camera Module 2
- HDMI display
- Push button (connected to GPIO17)
- Raspberry Pi OS (32-bit) with Desktop

## Pre-Installation Steps

1. Install Raspberry Pi OS with Desktop:
   - Download Raspberry Pi OS (32-bit) with Desktop from the official website
   - Use Raspberry Pi Imager to write the OS to your SD card

2. Enable the camera interface:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options > Camera > Enable
   ```

3. Enable SSH (if installing remotely):
   - Use raspi-config: Interface Options > SSH > Enable
   - Or create an empty file named 'ssh' in the boot partition

## Installation

1. Connect to your Pi via SSH:
   ```bash
   ssh pi@raspberrypi.local   # Default hostname
   # or
   ssh pi@<your-pi-ip-address>
   ```

2. Install git and clone the repository:
   ```bash
   sudo apt-get update
   sudo apt-get install -y git
   git clone https://https://github.com/Incognitonz/pi-camera-display.git
   cd pi-camera-display
   ```

3. Run the installation script:
   ```bash
   sudo chmod +x scripts/install.sh
   sudo ./scripts/install.sh
   ```

4. Reboot the Pi:
   ```bash
   sudo reboot
   ```

## Hardware Setup

After software installation:
1. Power off the Raspberry Pi
2. Connect the Camera Module 2 to the CSI port
3. Connect a button between GPIO17 and GND
4. Connect the HDMI display
5. Power on the Pi

## Configuration

Settings can be modified in `config/settings.py`:
- GPIO_BUTTON_PIN: GPIO pin for wake button (default: 17)
- SCREEN_SAVER_TIMEOUT: Screen saver timeout in seconds (default: 120)
- CAMERA_RESOLUTION: Camera capture resolution (default: 1920x1080)
- CAMERA_FRAMERATE: Camera capture framerate (default: 30)

## Service Management

```bash
# Check service status
sudo systemctl status camera-display

# View detailed logs
sudo cat /var/log/camera-display.log

# Live log monitoring
sudo journalctl -u camera-display -f

# Restart service
sudo systemctl restart camera-display

# Stop service
sudo systemctl stop camera-display

# Start service
sudo systemctl start camera-display
```

## Troubleshooting

### Display Issues

1. Check X server status:
   ```bash
   # Verify X is running
   ps aux | grep X
   
   # Check if display is available
   echo $DISPLAY
   
   # Test X server access
   xhost
   ```

2. Verify display configuration:
   ```bash
   # Check connected displays
   tvservice -s
   
   # List display modes
   tvservice -m CEA
   
   # Force HDMI mode if needed
   tvservice -p
   ```

3. Common display fixes:
   ```bash
   # Reset X server permissions
   xhost +local:root
   
   # Restart X server
   sudo systemctl restart display-manager
   ```

### Camera Issues

1. Verify camera connection:
   ```bash
   vcgencmd get_camera
   # Should show: supported=1 detected=1
   ```

2. Test camera:
   ```bash
   libcamera-hello
   ```

3. Check camera permissions:
   ```bash
   sudo usermod -a -G video $USER
   ```

### Service Issues

If the service fails to start:

1. Check logs for errors:
   ```bash
   sudo cat /var/log/camera-display.log
   sudo journalctl -u camera-display -f
   ```

2. Verify permissions:
   ```bash
   sudo chown -R root:root /opt/pi-camera-display
   sudo chmod -R 755 /opt/pi-camera-display
   ```

3. Check Python environment:
   ```bash
   # Verify virtual environment
   ls -l /opt/pi-camera-display/venv/bin/python3
   
   # Test Python imports
   /opt/pi-camera-display/venv/bin/python3 -c "import cv2; import picamera2; import RPi.GPIO"
   ```

### Button Issues

1. Test GPIO input:
   ```bash
   # Check GPIO status
   raspi-gpio get 17
   
   # Monitor GPIO changes
   watch -n 0.1 "raspi-gpio get 17"
   ```

2. Verify wiring:
   - Ensure button is connected between GPIO17 and GND
   - Check for loose connections
   - Try a different GPIO pin (update settings.py if changed)

## Logs and Debugging

The application logs to multiple locations:

1. Main application log:
   ```bash
   sudo cat /var/log/camera-display.log
   ```

2. Systemd service log:
   ```bash
   sudo journalctl -u camera-display -f
   ```

3. X server log:
   ```bash
   sudo cat /var/log/Xorg.0.log
   ```

## Common Error Solutions

1. "Failed to create window":
   ```bash
   # Reset X server permissions
   xhost +local:root
   sudo systemctl restart camera-display
   ```

2. "Camera not found":
   ```bash
   # Enable camera interface
   sudo raspi-config
   # Reboot after enabling
   sudo reboot
   ```

3. "Permission denied":
   ```bash
   # Fix permissions
   sudo chown -R root:root /opt/pi-camera-display
   sudo chmod -R 755 /opt/pi-camera-display
   sudo systemctl restart camera-display
   ```

If issues persist after trying these solutions, check the logs for specific error messages and ensure all hardware is properly connected.
