from scapy.layers.l2 import ARP, Ether
from scapy.sendrecv import srp
import time


def find_ip_by_mac(target_mac, subnet="192.168.1.0/24", attempts=5, timeout=4):
    arp = ARP(pdst=subnet)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    for i in range(attempts):
        result = srp(packet, timeout=timeout, verbose=False)[0]
        for sent, received in result:
            if received.hwsrc.lower() == target_mac.lower():
                return received.psrc
        time.sleep(1)

    return None