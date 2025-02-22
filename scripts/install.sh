#!/bin/bash

# Exit on any error
set -e

echo "Installing Raspberry Pi Camera Display System..."

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-opencv

# Create installation directory
echo "Creating installation directory..."
install_dir="/opt/pi-camera-display"
mkdir -p $install_dir

# Copy application files
echo "Copying application files..."
cp -r ../* $install_dir/

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r $install_dir/requirements.txt

# Install and enable systemd service
echo "Installing systemd service..."
cp $install_dir/service/camera-display.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable camera-display.service
systemctl start camera-display.service

echo "Installation complete!"
echo "The camera display system will start automatically on boot."
echo "To check the status, run: systemctl status camera-display"
