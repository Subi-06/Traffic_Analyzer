# Scapy simulation script
# Note: Requires scapy and admin privileges to run.
# This script will be called by the backend or run separately to simulate packets.

from scapy.all import IP, TCP, send
import random
import time

def simulate_traffic(target_ip="127.0.0.1", intensity="normal"):
    print(f"Starting traffic simulation: {intensity}")
    while True:
        pkt = IP(dst=target_ip)/TCP(dport=80)
        send(pkt, verbose=False)
        
        if intensity == "attack":
            time.sleep(0.01)
        else:
            time.sleep(random.uniform(0.1, 0.5))

if __name__ == "__main__":
    # Example usage
    # simulate_traffic(intensity="normal")
    pass
