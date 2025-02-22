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

## Installation

1. Connect the hardware:
   - Connect Camera Module 2 to the CSI port
   - Connect HDMI display
   - Connect button between GPIO17 and GND

2. Clone this repository and install:
   ```bash
   git clone [repository-url]
   cd pi-camera-display
   sudo chmod +x scripts/install.sh
   sudo ./scripts/install.sh
   ```

## Configuration

Configuration settings can be modified in `config/settings.py`:
- GPIO_BUTTON_PIN: GPIO pin for wake button (default: 17)
- SCREEN_SAVER_TIMEOUT: Screen saver timeout in seconds (default: 120)
- CAMERA_RESOLUTION: Camera capture resolution (default: 1920x1080)
- CAMERA_FRAMERATE: Camera capture framerate (default: 30)

## Usage

The system will start automatically on boot. The display will:
- Show camera feed on startup
- Enter screen saver mode after 2 minutes of inactivity
- Wake from screen saver when the button is pressed

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
```

## Troubleshooting

1. Check service status:
   ```bash
   sudo systemctl status camera-display
   ```

2. View logs:
   ```bash
   sudo journalctl -u camera-display -f
   ```

3. Common issues:
   - Black screen: Check HDMI connection and display settings
   - No camera feed: Check camera module connection and enable camera interface
   - Button not working: Check GPIO wiring and connections
