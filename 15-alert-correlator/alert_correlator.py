import argparse
import json
# TODO: sliding window approach would be better than fixed time bucket
# good enough for now
from collections import defaultdict

DEMO_EVENTS = [
    {"time": "2024-01-15 08:01:22", "src_ip": "192.168.1.50", "type": "failed_login", "dest": "server01"},
    {"time": "2024-01-15 08:01:25", "src_ip": "192.168.1.50", "type": "failed_login", "dest": "server01"},
    {"time": "2024-01-15 08:01:29", "src_ip": "192.168.1.50", "type": "failed_login", "dest": "server01"},
    {"time": "2024-01-15 08:01:33", "src_ip": "192.168.1.50", "type": "failed_login", "dest": "server01"},
    {"time": "2024-01-15 08:01:37", "src_ip": "192.168.1.50", "type": "failed_login", "dest": "server01"},
    {"time": "2024-01-15 08:02:10", "src_ip": "192.168.1.50", "type": "port_scan", "dest": "server01"},
    {"time": "2024-01-15 08:05:00", "src_ip": "10.0.0.99", "type": "malware_detected", "dest": "workstation03"},
    {"time": "2024-01-15 08:05:45", "src_ip": "10.0.0.99", "type": "dns_beacon", "dest": "8.8.8.8"},
    {"time": "2024-01-15 08:06:12", "src_ip": "10.0.0.99", "type": "data_exfil", "dest": "external.evil.com"},
    {"time": "2024-01-15 08:10:00", "src_ip": "172.16.0.5", "type": "failed_login", "dest": "db01"},
    {"time": "2024-01-15 08:12:00", "src_ip": "172.16.0.5", "type": "sql_injection", "dest": "db01"},
    {"time": "2024-01-15 08:13:30", "src_ip": "172.16.0.5", "type": "privilege_escalation", "dest": "db01"},
    {"time": "2024-01-15 08:20:00", "src_ip": "203.0.113.7", "type": "failed_login", "dest": "vpn01"},
]

def load_events(filepath):
    events = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    return events

def group_by_source(events):
    groups = defaultdict(list)
    for event in events:
        groups[event["src_ip"]].append(event)
    return groups

def get_unique_types(events_for_ip):
    types = set()
    for event in events_for_ip:
        types.add(event["type"])
    return types

def classify_source(events_for_ip):
    types = get_unique_types(events_for_ip)
    count = len(events_for_ip)

    if len(types) >= 3:
        return "CRITICAL", "Multiple attack types from same source (possible APT)"
    if count >= 5:
        return "HIGH", "High alert volume from this IP (possible automated attack)"
    if len(types) >= 2:
        return "MEDIUM", "More than one alert type detected from this source"
    return "LOW", "Single alert type, low volume"

def print_report(groups):
    print("\n=== Alert Correlation Report ===\n")
    order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    sorted_ips = sorted(groups.keys(), key=lambda ip: order[classify_source(groups[ip])[0]])

    for ip in sorted_ips:
        events = groups[ip]
        types = get_unique_types(events)
        severity, reason = classify_source(events)

        print(f"Source IP : {ip}")
        print(f"  Severity : {severity}")
        print(f"  Alerts   : {len(events)}")
        print(f"  Types    : {', '.join(sorted(types))}")
        print(f"  Reason   : {reason}")
        print()

def main():
    parser = argparse.ArgumentParser(description="SOC Alert Correlator")
    parser.add_argument("--file", help="Path to newline-delimited JSON events file")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo data")
    args = parser.parse_args()

    if args.demo:
        events = DEMO_EVENTS
    elif args.file:
        events = load_events(args.file)
    else:
        print("Provide --demo to run demo mode or --file <path> to load events.")
        return

    groups = group_by_source(events)
    print_report(groups)

if __name__ == "__main__":
    main()
