#!/usr/bin/env python3
import random
import socket
import sys
import argparse
from random import choice
from string import ascii_uppercase

from scapy.all import (
    IP, TCP, Ether, get_if_hwaddr, get_if_list, sendp
    )
from query_h import Query, Index

def get_if():
    ifs=get_if_list()
    iface=None # "h1-eth0"
    for i in get_if_list():
        if "eth0" in i:
            iface=i
            break
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface

def get_message():
    msg_size = random.randint(50, 100)
    return ''.join(choice(ascii_uppercase) for i in range(msg_size))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dest_addr', type=str, help="Destination IP address")
    parser.add_argument('pkt_type', type=int, default=None, help='1. Send normal packets  2. Send a query packet')
    parser.add_argument('pkt_num', type=int, default=None, help='Decide how many normal packets to send')
    args = parser.parse_args()
    
    addr = socket.gethostbyname(args.dest_addr)
    iface = get_if()

    query_msg = "This is a query packet"
    if(args.pkt_type == 1):
        pkt_list = list()
        for i in range(args.pkt_num):
            #print("sending on interface %s to %s" % (iface, str(addr)))
            pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
            pkt = pkt / Index() / IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / get_message()
            #pkt.show2()
            pkt_list.append(pkt)
        sendp(pkt_list, iface=iface, verbose=False)
    elif(args.pkt_type == 2):
        print("sending on interface %s to %s" % (iface, str(addr)))
        pkt =  Ether(src=get_if_hwaddr(iface), dst='ff:ff:ff:ff:ff:ff')
        pkt = pkt / Query() / IP(dst=addr) / TCP(dport=1234, sport=random.randint(49152,65535)) / query_msg
        pkt.show2()
        sendp(pkt, iface=iface, verbose=False)


if __name__ == '__main__':
    main()
