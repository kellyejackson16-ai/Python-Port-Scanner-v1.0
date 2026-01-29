import socket
import argparse
import threading
from colorama import Fore, Style, init
init()
from datetime import datetime

def scan_port(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)

    try:
       s.connect((host, port))
       try:
          banner = s.recv(1024).decode().strip()
       except:
           banner = "No banner"
       return True, banner
    except:
        return False, None
    finally:
        s.close()

def thread_worker(host, port):
    is_open, banner = scan_port(host, port)
    if is_open:
        print(f"{Fore.GREEN}[+] Port {port} is OPEN{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Banner: {banner}{Style.RESET_ALL}")
        write_log(f"[{datetime.now()}] Port {port} OPEN - Banner: {banner}")

def write_log(message):
    with open("scan_results.txt", "a") as f:
        f.write(message + "\n")

parser = argparse.ArgumentParser(description="Simple Python Port Scanner")
parser.add_argument("-H", "--host", required=True, help="Target host to scan")
parser.add_argument("-p", "--ports", required=True, help="Port range, e.g. 1-1024")

args = parser.parse_args()

host = args.host
start_port, end_port = map(int, args.ports.split("-"))

write_log("\n" + "="*50)
write_log(f"Scan started: {datetime.now()}")
write_log(f"Target: {host}")
write_log(f"Port range: {start_port}-{end_port}")
write_log("="*50)


# Parse the port range
start_port, end_port = map(int, args.ports.split("-"))

threads = []

for port in range(start_port, end_port + 1):
    t = threading.Thread(target=thread_worker, args=(host, port))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
