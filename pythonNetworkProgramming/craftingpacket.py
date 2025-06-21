from scapy.all import *

packet = IP(dst="8.8.8.8")/ICMP()
packet.show()
# Send the crafted packet
send(packet)