from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
from tabulate import tabulate

packets = rdpcap('captured_packets.pcap')
flows = {}

for packet in packets:
    if packet.haslayer(IP):
        timestamp = packet.time  # Epoch time
        if packet.haslayer(TCP):
            protocol = "TCP"
            sport = packet[TCP].sport
            dport = packet[TCP].dport
            payload_len = len(packet[TCP].payload)
        elif packet.haslayer(UDP):
            protocol = "UDP"
            sport = packet[UDP].sport
            dport = packet[UDP].dport
            payload_len = len(packet[UDP].payload)
        else:
            continue

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        flow_key = (protocol, src_ip, dst_ip, sport, dport)

        if flow_key not in flows:
            flows[flow_key] = {
                "count": 0,
                "start_time": timestamp,
                "end_time": timestamp,
                "total_payload": 0,
            } 

        flows[flow_key]["count"] += 1
        flows[flow_key]["end_time"] = timestamp
        flows[flow_key]["total_payload"] += payload_len

# Prepare data for tabulation
flows_list = []
for (proto, src_ip, dst_ip, sport, dport), stats in flows.items():
    duration = stats["end_time"] - stats["start_time"]
    avg_payload = stats["total_payload"] / stats["count"] if stats["count"] > 0 else 0
    flows_list.append([
        proto,
        src_ip,
        sport,
        dst_ip,
        dport,
        stats["count"],
        round(duration, 6),
        round(avg_payload, 2)
    ])

# Print the results
print(tabulate(
    flows_list,
    headers=["Protocol", "Source IP", "Source Port", "Destination IP", "Destination Port",
             "Packet Count", "Duration (s)", "Avg Payload (bytes)"],
    tablefmt="grid"
))

















# from scapy.all import *
# from collections import defaultdict
# import time

# # Dictionary to store flow information
# flow_stats = defaultdict(lambda: {
#     'packet_count': 0,
#     'start_time': None,
#     'end_time': None,
#     'total_payload': 0
# })

# def process_packet(pkt):
#     # Extract 5-tuple flow key
#     if not pkt.haslayer(IP):
#         return
    
#     flow_key = (
#         pkt[IP].src, 
#         pkt[IP].dst,
#         pkt[TCP].sport if pkt.haslayer(TCP) else pkt[UDP].sport if pkt.haslayer(UDP) else None,
#         pkt[TCP].dport if pkt.haslayer(TCP) else pkt[UDP].dport if pkt.haslayer(UDP) else None,
#         pkt[IP].proto
#     )
    
#     # Skip if not TCP/UDP (no ports)
#     if flow_key[2] is None or flow_key[3] is None:
#         return
    
#     # Get current timestamp
#     current_time = time.time()
    
#     # Initialize or update flow stats
#     if flow_stats[flow_key]['start_time'] is None:
#         flow_stats[flow_key]['start_time'] = current_time
    
#     flow_stats[flow_key]['end_time'] = current_time
#     flow_stats[flow_key]['packet_count'] += 1
    
#     # Calculate payload size (IP layer and above)
#     if pkt.haslayer(Raw):
#         payload_size = len(pkt[Raw].load)
#     else:
#         payload_size = 0
    
#     flow_stats[flow_key]['total_payload'] += payload_size

# # Start sniffing (adjust interface as needed)
# print("Starting packet capture... (Ctrl+C to stop)")
# sniff(prn=process_packet, store=False)

# # After capture stops, print results
# print("\nFlow Statistics:")
# print("{:<20} {:<20} {:<8} {:<8} {:<8} {:<10} {:<10} {:<12} {:<12}".format(
#     "Source IP", "Dest IP", "Sport", "Dport", "Proto", "Packets", "Duration(s)", 
#     "Avg Payload", "Total Bytes"
# ))

# for flow, stats in flow_stats.items():
#     src_ip, dst_ip, sport, dport, proto = flow
#     duration = stats['end_time'] - stats['start_time']
#     avg_payload = stats['total_payload'] / stats['packet_count'] if stats['packet_count'] > 0 else 0
    
#     print("{:<20} {:<20} {:<8} {:<8} {:<8} {:<10} {:<10.2f} {:<12.2f} {:<12}".format(
#         src_ip, dst_ip, sport, dport, proto, 
#         stats['packet_count'], duration, avg_payload, stats['total_payload']
#     ))