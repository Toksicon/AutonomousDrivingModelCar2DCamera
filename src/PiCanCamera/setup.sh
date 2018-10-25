#!/usr/bin/env bash
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python3-dev python3-pip -y
sudo pip3 install picamera
#sudo raspi-config #->enable camera
sudo pip3 install numpy
sudo apt-get install libatlas-base-dev -y
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
echo "dtoverlay=mcp2515-can0-overlay,oscillator=16000000,interrupt=25" | sudo tee -a /boot/config.txt
echo "dtoverlay=spi-bcm2835-overlay" | sudo tee -a /boot/config.txt
sudo python3 /home/pi/can/setup.py install
sudo /sbin/ip link set can0 up type can bitrate 500000