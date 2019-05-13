#!/usr/bin/env python
import subprocess,csv

maclist = []
signallist = []
iplist = []
hostlist = []

leasefile="/var/lib/misc/dnsmasq.leases"
# Retrieves Interface (wlan0)
def get_interface():
    p1 = subprocess.Popen(["netstat", "-i"], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["awk", '$1 ~ /^w/ {print $1}'], stdin=p1.stdout, stdout=subprocess.PIPE)
    displayInt= p2.communicate()[0].rstrip()
    return displayInt

# Store returned value in global variable
displayInt = get_interface()

# Retrieves MAC address
def get_mac():
    p3 = subprocess.Popen(["iw", "dev", displayInt, "station", "dump"], stdout=subprocess.PIPE)
    p4 = subprocess.Popen(["grep", "Station"], stdin=p3.stdout, stdout=subprocess.PIPE)
    p5 = subprocess.Popen(["cut", "-f", "2", "-s", "-d", " "], encoding="utf8", stdin=p4.stdout, stdout=subprocess.PIPE) # encoding is for getting a string (Normally in bytes)

    for line in p5.stdout:
        maclist.append(line.rstrip('\n'))
    return print(maclist)

# Retrieves Device Signal (dBm)
def get_signal():
    p6 = subprocess.Popen(["iw", "dev", displayInt, "station", "dump"], stdout=subprocess.PIPE)
    p7 = subprocess.Popen(["grep", "signal:"], stdin=p6.stdout, stdout=subprocess.PIPE)
    p8 = subprocess.Popen(["awk", '{print $2}'], encoding="utf8", stdin=p7.stdout, stdout=subprocess.PIPE)

    for line in p8.stdout:
        signallist.append(line.rstrip('\n'))            # rstrip() removes every newline
    return print(signallist)

# Retrieves IP and Hostname
def get_ip():
    with open(leasefile,'r') as infile:
        # Prints the 2nd and 3rd coulumn of file
        column = [ cols[2:4] for cols in csv.reader(infile, delimiter=" ") ]

    # Takes the columns
    iplist = [x[0] for x in column]
    return print(iplist)

def get_host():
    with open(leasefile,'r') as infile:
        # Prints the 2nd and 3rd coulumn of file
        column = [ cols[2:4] for cols in csv.reader(infile, delimiter=" ") ]
    hostlist = [x[1] for x in column]
    return print(hostlist)
