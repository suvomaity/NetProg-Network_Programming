from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from tabulate import tabulate

interface = "Wi-Fi"  
capture_duration = 10  
output_file = "captured_packets.pcap"  



# 2. Start packet capture
print(f"Starting capture on interface {interface} for {capture_duration} seconds...")
packets = sniff(iface=interface, timeout=capture_duration)



# 3. Save captured packets to file
wrpcap(output_file, packets)
print(f"Captured {len(packets)} packets and saved to {output_file}")

