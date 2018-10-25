sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install python3-dev python3-pip -y
sudo pip3 install picamera
#sudo raspi-config #->enable camera
sudo pip3 install numpy
sudo apt-get install libatlas-base-dev -y
echo "dtparam=spi=on" | sudo tee -a /boot/config.txt
echo "dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25" | sudo tee -a /boot/config.txt
echo "dtoverlay=spi-bcm2835-overlay" | sudo tee -a /boot/config.txt
sudo python3 /home/pi/can/setup.py install
#sudo /sbin/ip link set can0 up type can bitrate 500000

#WIFI
sudo apt-get install hostapd -y
sudo apt-get install dnsmasq -y

#stop services for now
sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

#config wlan0 interface
sudo echo 'interface wlan0' | sudo tee -a /etc/dhcpcd.conf
sudo echo 'static ip_address=192.168.0.10/24' | sudo tee -a /etc/dhcpcd.conf
sudo echo 'nohook wpa_supplicant' | sudo tee -a /etc/dhcpcd.conf
sudo echo 'denyinterfaces wlan0' | sudo tee -a /etc/dhcpcd.conf

#define ip-range for clients
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo echo 'interface=wlan0' | sudo tee -a /etc/dnsmasq.conf
sudo echo 'dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,24h' | sudo tee -a /etc/dnsmasq.conf

#wifi config
sudo echo 'interface=wlan0' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'hw_mode=g' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'channel=7' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'wmm_enabled=0' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'macaddr_acl=0' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'auth_algs=1' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'ignore_broadcast_ssid=0' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'wpa=2' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'wpa_key_mgmt=WPA-PSK' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'wpa_pairwise=TKIP' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'rsn_pairwise=CCMP' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'ssid=alamak2018' | sudo tee -a /etc/hostapd/hostapd.conf
sudo echo 'wpa_passphrase=alamak2018' | sudo tee -a /etc/hostapd/hostapd.conf

#Tell system
sudo echo 'DAEMON_CONF="/etc/hostapd/hostapd.conf"' | sudo tee -a /etc/default/hostapd

#IP-Tables
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
iptables-restore < /etc/iptables.ipv4.nat

#start services for now
sudo systemctl start hostapd
sudo systemctl start dnsmasq