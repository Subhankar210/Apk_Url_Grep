#!/bin/bash

# Check if the script is being run as root
if [ "$(id -u)" -ne 0 ]; then
  echo "This script must be run as root (use sudo)"
  exit 1
fi

# Give execute permissions to apktool and apktool.jar
chmod +x apktool
chmod +x apktool.jar

# Move apktool and apktool.jar to /usr/local/bin
echo "Moving apktool and apktool.jar to /usr/local/bin..."
mv apktool /usr/local/bin/
mv apktool.jar /usr/local/bin/

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "Installation complete!"
