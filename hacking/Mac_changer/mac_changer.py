#!/usr/bin/env python

import subprocess
import optparse
import re

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)

    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("[-] MAC address not found.")
#this will return the current mac address of interface eg: eth0
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface will change its mac address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New Mac Address")

    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.mac_address:
        parser.error("[-] please specify a new mac, use --help for more info")
    return options
# arguments are --i,--interface,--mac,-m


def mac_changer(interface, mac_address):
    print("[+] Changing old mac adress of " + interface + " to " + mac_address)

    # subprocess.call("ifconfig "+ interface +" down",shell=True)
    # subprocess.call("ifconfig "+ interface +" hw ether "+ mac_address,shell=True)
    # subprocess.call("ifconfig "+ interface +" up",shell=True)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])
#thiss is our first function we have made in starting that change the mac address of target interface.

# options will take values from the user and parse the value


options = get_arguments()

current_mac_address = get_current_mac(options.interface)
print("Current Mac = " + str(current_mac_address))

mac_changer(options.interface, options.mac_address)

current_mac_address = get_current_mac(options.interface)

if current_mac_address == options.mac_address:
    print("[+] Mac Address was successfully changed to " + current_mac_address)
else:
    print("[-] Mac Address did not change")