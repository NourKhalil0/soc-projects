#!/usr/bin/env python3

import argparse
import socket
from datetime import datetime

COMMON_PORTS = {
    21:   "FTP",
    22:   "SSH",
    23:   "Telnet",
    25:   "SMTP",
    53:   "DNS",
    80:   "HTTP",
    110:  "POP3",
    135:  "RPC",
    139:  "NetBIOS",
    143:  "IMAP",
    443:  "HTTPS",
    445:  "SMB",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def scan_port(ip, port, timeout):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    result = sock.connect_ex((ip, port))
    sock.close()
    return result == 0


def scan_target(ip, ports, timeout):
    open_ports = []
    for port in ports:
        if scan_port(ip, port, timeout):
            service = COMMON_PORTS.get(port, "Unknown")
            open_ports.append((port, service))
    return open_ports


def print_report(host, ip, open_ports, scanned, start_time):
    duration = (datetime.now() - start_time).seconds
    print("\n========================================")
    print("           PORT SCANNER REPORT")
    print("========================================")
    print(f"Host     : {host}")
    print(f"IP       : {ip}")
    print(f"Ports    : {scanned} scanned")
    print(f"Time     : {duration}s")
    print("========================================\n")

    if not open_ports:
        print("No open ports found.\n")
        return

    print(f"{'PORT':<8} {'SERVICE':<14} {'STATUS'}")
    print("-" * 34)
    for port, service in open_ports:
        print(f"{port:<8} {service:<14} OPEN")

    print(f"\n{len(open_ports)} open port(s) found.\n")
    print("========================================\n")


def get_ports(args):
    if args.ports:
        ports = []
        for part in args.ports.split(","):
            part = part.strip()
            if "-" in part:
                start, end = part.split("-")
                ports.extend(range(int(start), int(end) + 1))
            else:
                ports.append(int(part))
        return ports
    if args.all:
        return list(range(1, 1025))
    return list(COMMON_PORTS.keys())


def main():
    parser = argparse.ArgumentParser(description="Scan a host for open ports")
    parser.add_argument("host", nargs="?", default="scanme.nmap.org", help="Target host or IP")
    parser.add_argument("-p", "--ports", help="Ports to scan, e.g. 22,80 or 20-100")
    parser.add_argument("-a", "--all", action="store_true", help="Scan ports 1 to 1024")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout per port in seconds")
    parser.add_argument("--demo", action="store_true", help="Scan scanme.nmap.org as a demo")
    args = parser.parse_args()

    host = "scanme.nmap.org" if args.demo else args.host

    print(f"\nResolving {host}...")
    ip = resolve_host(host)
    if not ip:
        print(f"Could not resolve {host}")
        return

    ports = get_ports(args)
    print(f"Scanning {len(ports)} ports on {ip}...\n")

    start_time = datetime.now()
    open_ports = scan_target(ip, ports, args.timeout)
    print_report(host, ip, open_ports, len(ports), start_time)


if __name__ == "__main__":
    main()
