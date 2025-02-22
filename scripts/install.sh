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
    python3-venv

# Create installation directory
echo "Creating installation directory..."
install_dir="/opt/pi-camera-display"
sudo mkdir -p $install_dir

# Create virtual environment
echo "Creating Python virtual environment..."
sudo python3 -m venv $install_dir/venv

# Copy application files
echo "Copying application files..."
sudo cp -r ../* $install_dir/

# Update service file to use virtual environment Python
sudo sed -i "s|ExecStart=/usr/bin/python3|ExecStart=$install_dir/venv/bin/python3|g" $install_dir/service/camera-display.service

# Install and enable systemd service
echo "Installing systemd service..."
sudo cp $install_dir/service/camera-display.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable camera-display.service
sudo systemctl start camera-display.service

echo "Installation complete!"
echo "The camera display system will start automatically on boot."
echo "To check the status, run: systemctl status camera-display"
