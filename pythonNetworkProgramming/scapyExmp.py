from scapy.all import sniff, TCP, UDP , ICMP

tcp_count = 0
udp_count = 0
icmp_count = 0
tcp_payload = 0
udp_payload =0
icmp_payload = 0
total_payload = 0
payload_count = 0

def analyze_packet(pkt):
    global tcp_count, udp_count, total_payload, payload_count,tcp_payload,udp_payload,icmp_count,icmp_payload

    if TCP in pkt:
        tcp_count += 1
        payload = bytes(pkt[TCP].payload)
        tcp_payload += len(payload)
    elif UDP in pkt:
        udp_count += 1
        payload = bytes(pkt[UDP].payload)
        udp_payload += len(payload)
    elif ICMP in pkt:
        icmp_count += 1
        payload = bytes(pkt[ICMP].payload)
        icmp_payload += len(payload)
    else:
        payload = b''

    if payload:
        total_payload += len(payload)
        payload_count += 1

    print(len(payload),pkt.summary()) # Show summary in terminal

# Capture and analyze 100 packets live
sniff(count=50, prn=analyze_packet)

avg_payload = total_payload / payload_count if payload_count else 0
udp_avg = udp_payload / udp_count if udp_count else 0
tcp_avg = tcp_payload / tcp_count if tcp_count else 0
icmp_avg = icmp_payload / icmp_count if icmp_count else 0

print(f"\nFinal stats:")
print(f"TCP Packets: {tcp_count} : Tcp payload : {tcp_payload} avg: {tcp_avg}")
print(f"UDP Packets: {udp_count} : UDP payload : {udp_payload} avg: {udp_avg}")
print(f"icmp Packets: {icmp_count} : UDP payload : {icmp_payload} avg: {icmp_avg}")
print(f" Total payload: {total_payload}")
print(f"Average Payload Length: {avg_payload:.2f} bytes")