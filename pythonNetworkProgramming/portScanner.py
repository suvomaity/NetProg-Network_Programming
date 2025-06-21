# Port Scanner using Scapy

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP

host = input("Enter target IP: ")
ports = input("Enter ports to scan (comma-separated): ").split(",")
ports = [int(p.strip()) for p in ports]

print(f"\nScanning {host} on ports {ports}...\n")

for port in ports:
    pkt = IP(dst=host) / TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=1, verbose=0)

    if resp is None:
        print(f"[?] Port {port} is filtered or no response")
    elif resp.haslayer(TCP):
        if resp[TCP].flags == 0x12:
            print(f"[+] Port {port} is OPEN")
        elif resp[TCP].flags == 0x14:
            print(f"[-] Port {port} is CLOSED") 
    else:
        print(f"[!] Unknown response on port {port}")


# import re
# from scapy.all import *

# try:
#     host = input("Enter a host address: ")
#     p = list(input("Enter the ports to scan (comma-separated): ").split(","))
#     temp = map(int, p)
#     ports = list(temp)

#     if(re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", host)):
#         print("\n\nScanning...")
#         print("Host: ", host)
#         print("Ports: ", ports)

#         ans, unans = sr(IP(dst=host)/TCP(dport=ports, flags="S"), verbose=0, timeout=2)

#         for (s, r) in ans:
#             print("[+] {} Open".format(s[TCP].dport))
#     else:
#         print("[-] Invalid IP address format. Exiting.")

# except (ValueError, RuntimeError, TypeError, NameError) as e:
#     print("[-] An error occurred:", e)
#     print("[-] Exiting..")
