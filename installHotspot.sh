#!/bin/bash

pkg1=dnsmasq
pkg2=hostapd
pkg3=bridge-utils
eth0=$(netstat -i | column -t | grep ^e | cut -f 1 -d" ")
wlan0=$(netstat -i | column -t | grep ^w | cut -f 1 -d" ")

if [ "$(id -u)" != "0" ]; then
	echo "Run it as root"
	exit 1
fi

PKG_OK=$(dpkg-query -W --showformat='${Status}\n' $pkg1 $pkg2 $pkg3 | grep "install ok installed" | wc -l)
echo Checking for packages: $pkg1 $pkg2 $pkg3
if [[ "0" == "$PKG_OK" || "1" == "$PKG_OK" || "2" == "$PKG_OK" ]]; then
  sudo apt-get --yes install $pkg1 $pkg2 $pkg3
else
    echo "All mandatory packages are installed"
fi
sleep 1

sudo systemctl stop $pkg1
sleep 1
sudo systemctl stop $pkg2
sleep 1

if [ ! -f /etc/dhcpcd.conf ]; then
    sudo echo "denyinterfaces $eth0" >> /etc/dhcpcd.conf
    sudo echo "denyinterfaces $wlan0" >> /etc/dhcpcd.conf

    sudo printf "interface $wlan0
        static ip_adress=192.168.4.1/24
        nohook wpa_supplicant\n" >> /etc/dhcpcd.conf
fi
sleep 1

sudo service dhcpcd restart
sleep 1

if [ ! -f /etc/dnsmasq.conf.orig ]; then
    sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
fi

if ! grep -q "interface=$wlan0
    dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h\n" /etc/dnsmasq.conf; then
    sudo printf "interface=$wlan0
        dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h\n" >> /etc/dnsmasq.conf
fi

if [ ! -f /etc/hostapd/hostapd.conf ]; then
    sudo printf "interface=$wlan0
    bridge=br0
    ssid=NameOfNetwork
    hw_mode=g
    channel=7
    wmm_enabled=0
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase=password
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=TKIP
    rsn_pairwise=CCMP\n" > /etc/hostapd/hostapd.conf
    echo "Insert network name: "
    read networkName
    echo "Insert password: "
    read password
    sudo sed -i "s/NameOfNetwork/$networkName/" /etc/hostapd/hostapd.conf
    sudo sed -i "s/password/$password/" /etc/hostapd/hostapd.conf
fi

if [ ! -f /etc/default/hostapd.orig ]; then
    sudo cp /etc/default/hostapd /etc/default/hostapd.orig
fi
sudo sed -i 's+#DAEMON_CONF=""+DAEMON_CONF=/etc/hostapd/hostapd.conf+' /etc/default/hostapd

# sudo systemctl start hostapd
# sleep 1
# sudo systemctl start dnsmasq
# sleep 1

sudo sed -i 's/#net.ipv4.ip_forward=1/net.ipv4.ip_forward=1/' /etc/sysctl.conf

##########
if [[ "$(ifconfig | grep br0 |  wc -l)" == "0" ]]; then
    sudo brctl addbr br0
    sudo brctl addif br0 $eth0
fi

if ! grep -q "Bridge setup" /etc/network/interfaces; then
    sudo printf "\n# Bridge setup
    auto br0
    iface br0 inet manual
    bridge_ports $eth0 $wlan0\n" >> /etc/network/interfaces
fi

sudo systemctl start hostapd
sudo systemctl start dnsmasq

printf "\nReboot your system to apply changes.\n"

#/etc/network/interfaces
#/etc/dhcpcd.conf
#/etc/dnsmasq.conf
#/etc/hostapd/hostapd.conf
#/etc/default/hostapd
#/etc/sysctl.conf
