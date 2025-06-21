from scapy.all import IP, ICMP, sr1
import time

def scan_fake_ip_range(start=100, end=110):
    base_ip = "172.16.1."  # Assume fake IPs are in this range
    print("Scanning for active fake IPs...")

    for i in range(start, end + 1):
        ip = base_ip + str(i)
        pkt = IP(dst=ip)/ICMP()
        reply = sr1(pkt, timeout=1, verbose=0)

        if reply:
            print(f"[+] Host active at {ip}")
        else:
            print(f"[-] No response from {ip}")
        time.sleep(0.5)

scan_fake_ip_range()
