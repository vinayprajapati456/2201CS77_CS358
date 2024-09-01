from scapy.all import *
import time

def tracert(destination, max_ttl=30, timeout=2, pings_per_hop=3, delay_between_pings=1, output_file=None):
    results = []
    try:
        for ttl in range(1, max_ttl + 1):
            for _ in range(pings_per_hop):
                pkt = IP(dst=destination, ttl=ttl) / ICMP()
                start_time = time.time()
                reply = sr1(pkt, verbose=0, timeout=timeout)
                rtt = (time.time() - start_time) * 1000  # RTT in milliseconds
                if reply is None:
                    result = f"{ttl} * * * Request timed out."
                elif reply.type == 0:
                    result = f"{ttl} {reply.src} {rtt:.2f} ms Reached destination."
                    results.append(result)
                    break
                else:
                    result = f"{ttl} {reply.src} {rtt:.2f} ms"
                results.append(result)
                time.sleep(delay_between_pings)
            if reply and reply.type == 0:
                break

        if output_file:
            with open(output_file, 'w') as f:
                for line in results:
                    f.write(line + '\n')
        else:
            for line in results:
                print(line)
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    try:
        destination = input("Enter the destination IP: ")
        max_ttl = int(input("Enter the max TTL value: "))
        timeout = int(input("Enter the timeout value: "))
        pings_per_hop = int(input("Enter the number of pings per hop: "))
        delay_between_pings = int(input("Enter the delay between pings (in seconds): "))
        output_file = input("Enter the output file name (leave blank for console output): ")
        output_file = output_file if output_file else None

        tracert(destination, max_ttl, timeout, pings_per_hop, delay_between_pings, output_file)
    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
