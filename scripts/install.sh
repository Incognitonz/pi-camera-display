#!/bin/bash

# Exit on any error
set -e

echo "Installing Raspberry Pi Camera Display System..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3-full \
    python3-pip \
    python3-opencv \
    python3-numpy \
    python3-rpi.gpio \
    python3-picamera2 \
    python3-venv \
    xorg \
    x11-xserver-utils

# Create installation directory
echo "Creating installation directory..."
install_dir="/opt/pi-camera-display"
sudo mkdir -p $install_dir

# Create log file
echo "Setting up logging..."
sudo touch /var/log/camera-display.log
sudo chmod 644 /var/log/camera-display.log

# Create virtual environment
echo "Creating Python virtual environment..."
sudo python3 -m venv $install_dir/venv

# Copy application files
echo "Copying application files..."
sudo cp -r ../* $install_dir/

# Set up X11 for root
echo "Configuring display environment..."
if ! grep -q "xhost +local:root" /etc/profile; then
    echo "xhost +local:root" | sudo tee -a /etc/profile
fi

# Configure auto login and X server
echo "Configuring auto login..."
sudo raspi-config nonint do_boot_behaviour B2
sudo systemctl set-default graphical.target

# Update service file to use virtual environment Python
sudo sed -i "s|ExecStart=/usr/bin/python3|ExecStart=$install_dir/venv/bin/python3|g" $install_dir/service/camera-display.service

# Install and enable systemd service
echo "Installing systemd service..."
sudo cp $install_dir/service/camera-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable camera-display.service

echo "Installation complete!"
echo "Please reboot your Raspberry Pi to start the camera display system."
echo "After reboot, check the logs with: sudo cat /var/log/camera-display.log"
echo "To check service status: sudo systemctl status camera-display"
