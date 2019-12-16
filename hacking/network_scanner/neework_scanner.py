#!/usr/bin/env python

import scapy.all as scapy
import optparse
#argparse
def get_arguments():
    parser = optparse.OptionParser()  #ArgumentParser()
    parser.add_option("--t", "--target", dest="target", help="You have to enter the range of IP to send and recieve Mac Address Upto:")
        #add_argument
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify an target, use --help for more info.")
    return options

def scan(ip):
    arp_result = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_result
    answered_list  = scapy.srp(arp_request_broadcast, timeout=1, verbose = False)[0]
    #verbose = False is passed to hide the data of the srp function
    #timeout =1 is used to stop the function in 1 sec.
    #srp returns two lists , one is answered list and one is unanswered list but we only requires answered list.so we put[0] at the end of srp to return the answered list assigned at index 0

    client_list = []
    for item in answered_list:
        client_dict = {"ip":item[1].psrc,"mac":item[1].hwsrc}
        client_list.append(client_dict)

    #psrc is the ip of the client which receive the packet we send and
    #hwsrc is the mac address of the machine whose ip is given in hwsrc.
    return client_list
def print_result(result_list):
    print("IP\t\t\tMAC Address\n-----------------------------------------------------------------")
    for client in result_list:
        print(client["ip"]+"\t\t"+client["mac"])

options = get_arguments()
scan_result =scan(options.target)
print_result(scan_result)