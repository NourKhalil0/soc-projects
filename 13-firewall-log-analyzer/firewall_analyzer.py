import argparse
import re
from collections import defaultdict

DEMO_LOGS = [
    "2024-01-15 08:23:11 DENY TCP 192.168.1.100 -> 10.0.0.5:22",
    "2024-01-15 08:23:12 DENY TCP 192.168.1.100 -> 10.0.0.5:80",
    "2024-01-15 08:23:13 DENY TCP 192.168.1.100 -> 10.0.0.5:443",
    "2024-01-15 08:23:14 DENY TCP 192.168.1.100 -> 10.0.0.5:8080",
    "2024-01-15 08:23:15 DENY TCP 192.168.1.100 -> 10.0.0.5:3389",
    "2024-01-15 08:23:16 DENY TCP 192.168.1.100 -> 10.0.0.5:21",
    "2024-01-15 09:10:00 ALLOW TCP 10.0.0.50 -> 8.8.8.8:53",
    "2024-01-15 09:11:00 DENY TCP 203.0.113.45 -> 10.0.0.5:22",
    "2024-01-15 09:12:00 ALLOW UDP 10.0.0.20 -> 1.1.1.1:53",
    "2024-01-15 10:00:00 DENY TCP 198.51.100.22 -> 10.0.0.5:22",
    "2024-01-15 10:01:00 DENY TCP 198.51.100.22 -> 10.0.0.5:22",
    "2024-01-15 10:02:00 DENY TCP 198.51.100.22 -> 10.0.0.5:22",
    "2024-01-15 10:03:00 DENY TCP 198.51.100.22 -> 10.0.0.5:22",
    "2024-01-15 10:04:00 DENY TCP 198.51.100.22 -> 10.0.0.5:22",
]

def parse_line(line):
    pattern = r"(\S+ \S+) (ALLOW|DENY) (TCP|UDP) (\S+) -> (\S+):(\d+)"
    m = re.match(pattern, line.strip())
    if not m:
        return None
    return {"action": m.group(2), "src": m.group(4), "port": int(m.group(6))}

def load_file(filepath):
    entries = []
    with open(filepath) as f:
        for line in f:
            e = parse_line(line)
            if e:
                entries.append(e)
    return entries

def count_blocks(entries):
    counts = defaultdict(int)
    for e in entries:
        if e["action"] == "DENY":
            counts[e["src"]] += 1
    return counts

def detect_scan(entries, threshold=5):
    ports_seen = defaultdict(set)
    for e in entries:
        if e["action"] == "DENY":
            ports_seen[e["src"]].add(e["port"])
    return {ip: sorted(p) for ip, p in ports_seen.items() if len(p) >= threshold}

def top_ports(entries, n=5):
    counts = defaultdict(int)
    for e in entries:
        if e["action"] == "DENY":
            counts[e["port"]] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

def print_report(entries):
    blocked = sum(1 for e in entries if e["action"] == "DENY")
    print(f"\n=== Firewall Log Report ===")
    print(f"Total events  : {len(entries)}")
    print(f"Allowed       : {len(entries) - blocked}")
    print(f"Blocked       : {blocked}")
    ip_blocks = count_blocks(entries)
    print("\nTop blocked sources:")
    for ip, c in sorted(ip_blocks.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {ip:<22} {c} blocks")
    print("\nTop blocked ports:")
    for port, c in top_ports(entries):
        print(f"  Port {port:<8} {c} hits")
    for ip, ports in detect_scan(entries).items():
        print(f"\n[ALERT] Port scan from {ip}: {ports}")
    for ip, c in ip_blocks.items():
        if c >= 5:
            print(f"[ALERT] Brute force from {ip}: {c} blocked attempts")

def main():
    parser = argparse.ArgumentParser(description="Firewall Log Analyzer")
    parser.add_argument("--file", help="Path to firewall log file")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo data")
    args = parser.parse_args()
    if args.demo:
        entries = [parse_line(l) for l in DEMO_LOGS]
        print_report([e for e in entries if e])
    elif args.file:
        print_report(load_file(args.file))
    else:
        print("Use --demo to test, or --file <path> to analyze a log file.")

if __name__ == "__main__":
    main()
