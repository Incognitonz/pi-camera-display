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
- Raspberry Pi OS Lite (32-bit)

## Pre-Installation Steps

1. Enable the camera interface on your Raspberry Pi:
   ```bash
   sudo raspi-config
   # Navigate to: Interface Options > Camera > Enable
   ```

2. Enable SSH (if installing remotely):
   - Create an empty file named 'ssh' in the boot partition of SD card, or
   - Use raspi-config: Interface Options > SSH > Enable

## Installation Methods

### Method 1: SSH Installation (Recommended)

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
   git clone https://github.com/yourusername/pi-camera-display.git
   cd pi-camera-display
   ```

3. Run the installation script:
   ```bash
   sudo chmod +x scripts/install.sh
   sudo ./scripts/install.sh
   ```

### Method 2: Direct SD Card Copy

1. With the SD card mounted on your computer:
   - Copy the entire 'pi-camera-display' folder to /home/pi/
   - Create an empty 'ssh' file in the boot partition (if needed)

2. Insert the SD card into the Pi and power it on

3. Connect via SSH and install:
   ```bash
   cd /home/pi/pi-camera-display
   sudo chmod +x scripts/install.sh
   sudo ./scripts/install.sh
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

# Stop service
sudo systemctl stop camera-display

# Start service
sudo systemctl start camera-display

# Disable autostart
sudo systemctl disable camera-display

# Enable autostart
sudo systemctl enable camera-display

# View logs
sudo journalctl -u camera-display -f
```

## Troubleshooting

### Common Issues

1. Black screen:
   - Check HDMI connection
   - Verify display settings: `tvservice -s`
   - Check logs: `sudo journalctl -u camera-display -f`

2. No camera feed:
   - Verify camera connection
   - Confirm camera is enabled: `vcgencmd get_camera`
   - Check camera detection: `libcamera-hello`

3. Button not working:
   - Verify wiring connections
   - Test GPIO input: `raspi-gpio get 17`
   - Check button in logs: `sudo journalctl -u camera-display -f`

4. Installation errors:
   - If you see "externally-managed-environment" error, the install script will handle this by using system packages and a virtual environment
   - For other package issues, check: `sudo apt update` and try installation again

### Checking System Status

1. Camera interface status:
   ```bash
   vcgencmd get_camera
   ```
   Should show: `supported=1 detected=1`

2. Display detection:
   ```bash
   tvservice -s
   ```

3. GPIO status:
   ```bash
   raspi-gpio get 17
   ```

4. Service status:
   ```bash
   systemctl status camera-display
   ```

### Getting Help

If you encounter issues:
1. Check the service logs:
   ```bash
   sudo journalctl -u camera-display -f
   ```
2. Verify all hardware connections
3. Ensure all system dependencies are installed:
   ```bash
   sudo apt-get install -y python3-full python3-pip python3-opencv python3-numpy python3-rpi.gpio python3-picamera2
