from scapy.all import *
import time

def ping(destination, count=4, ttl=64, packet_size=64, timeout=2):
    sent_packets = 0
    received_packets = 0
    rtt_list = []

    try:
        for i in range(count):
            pkt = IP(dst=destination, ttl=ttl) / ICMP() / (b'X' * packet_size)
            start_time = time.time()
            reply = sr1(pkt, verbose=0, timeout=timeout)
            end_time = time.time()
            rtt = (end_time - start_time) * 1000  # RTT in milliseconds

            sent_packets += 1
            if reply is None:
                print(f"Request timed out.")
            else:
                received_packets += 1
                rtt_list.append(rtt)
                print(f"{reply.src} is alive, RTT: {rtt:.2f} ms")

        packet_loss = ((sent_packets - received_packets) / sent_packets) * 100
        avg_rtt = sum(rtt_list) / len(rtt_list) if rtt_list else 0
        max_rtt = max(rtt_list) if rtt_list else 0
        min_rtt = min(rtt_list) if rtt_list else 0

        print(f"\n--- {destination} ping statistics ---")
        print(f"{sent_packets} packets transmitted, {received_packets} received, {packet_loss:.2f}% packet loss")
        print(f"rtt min/avg/max = {min_rtt:.2f}/{avg_rtt:.2f}/{max_rtt:.2f} ms")

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        destination = input("Enter the destination IP: ")
        count = int(input("Enter the number of pings: "))
        ttl = int(input("Enter the TTL value: "))
        packet_size = int(input("Enter the packet size: "))
        timeout = int(input("Enter the timeout value: "))
        ping(destination, count, ttl, packet_size, timeout)
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
