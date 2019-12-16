#!/usr/bin/env python
import netfilterqueue

def process_packet(packet):
    print(packet)
    #packet.accept()
    packet.drop()
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
#in terminal  ---- iptables -I FORWARD -j NFQUEUE --queue-num 0
#do not miss to forward ip
#echo 1 > proc/sys/ipv4/ip_forward