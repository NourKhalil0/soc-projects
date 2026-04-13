import argparse
import socket
import sys
from datetime import datetime


def get_dns_records(domain):
    results = {"A": [], "AAAA": []}
    try:
        addresses = socket.getaddrinfo(domain, None)
        for entry in addresses:
            addr = entry[4][0]
            if entry[0] == socket.AF_INET and addr not in results["A"]:
                results["A"].append(addr)
            if entry[0] == socket.AF_INET6 and addr not in results["AAAA"]:
                results["AAAA"].append(addr)
    except socket.gaierror:
        pass
    return results


def get_reverse_dns(ip):
    try:
        return socket.getfqdn(ip)
    except Exception:
        return "N/A"


def print_report(domain, records, reverse_map):
    print("=" * 50)
    print("  Domain Info Lookup Report")
    print("=" * 50)
    print(f"  Domain:    {domain}")
    print(f"  Scanned:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    print("  DNS Records:")
    for rtype, values in records.items():
        if values:
            for v in values:
                print(f"    {rtype:6s} -> {v}")
        else:
            print(f"    {rtype:6s} -> (none)")
    print("-" * 50)
    print("  Reverse DNS:")
    for ip, hostname in reverse_map.items():
        print(f"    {ip} -> {hostname}")
    print("=" * 50)


def run_demo():
    domain = "example-target.com"
    records = {
        "A": ["93.184.216.34", "93.184.216.35"],
        "AAAA": ["2606:2800:220:1:248:1893:25c8:1946"],
    }
    reverse_map = {
        "93.184.216.34": "server1.example-target.com",
        "93.184.216.35": "server2.example-target.com",
    }
    print_report(domain, records, reverse_map)


def run_live(domain):
    records = get_dns_records(domain)
    reverse_map = {}
    for ip in records.get("A", []):
        reverse_map[ip] = get_reverse_dns(ip)
    print_report(domain, records, reverse_map)


def main():
    parser = argparse.ArgumentParser(description="Domain Info Lookup Tool")
    parser.add_argument("--domain", help="Domain to look up")
    parser.add_argument("--demo", action="store_true", help="Run with sample data")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.domain:
        run_live(args.domain)
    else:
        print("Error: use --domain <name> or --demo")
        sys.exit(1)


if __name__ == "__main__":
    main()
