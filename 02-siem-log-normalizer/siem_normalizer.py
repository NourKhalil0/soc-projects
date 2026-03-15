#!/usr/bin/env python3

import argparse
import re
import os
from datetime import datetime


SEVERITY_KEYWORDS = {
    "critical": ["root login", "accepted password for root", "sudo su", "privilege escalation"],
    "high":     ["failed password", "invalid user", "authentication failure", "error", "denied"],
    "medium":   ["warning", "timeout", "connection reset", "refused"],
    "low":      ["accepted", "opened", "started", "connected", "info"],
}

SOURCE_PATTERNS = {
    "ssh": re.compile(r"sshd\[", re.IGNORECASE),
    "sudo": re.compile(r"sudo\[|sudo:", re.IGNORECASE),
    "firewall": re.compile(r"iptables|ufw|firewall|BLOCKED|ACCEPT|DROP", re.IGNORECASE),
    "web": re.compile(r'"(GET|POST|PUT|DELETE|HEAD)', re.IGNORECASE),
    "system": re.compile(r"kernel|systemd|cron", re.IGNORECASE),
}

IP_PATTERN = re.compile(r"\b(\d{1,3}\.){3}\d{1,3}\b")
TIMESTAMP_PATTERN = re.compile(r"(\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2})")


def get_severity(line):
    line_lower = line.lower()
    for level in ["critical", "high", "medium", "low"]:
        for keyword in SEVERITY_KEYWORDS[level]:
            if keyword in line_lower:
                return level
    return "info"


def get_source(line):
    for source, pattern in SOURCE_PATTERNS.items():
        if pattern.search(line):
            return source
    return "unknown"


def get_ip(line):
    match = IP_PATTERN.search(line)
    if match:
        return match.group()
    return "N/A"


def get_timestamp(line):
    match = TIMESTAMP_PATTERN.search(line)
    if match:
        return match.group()
    return "N/A"


def normalize_line(line):
    return {
        "timestamp": get_timestamp(line),
        "source":    get_source(line),
        "severity":  get_severity(line),
        "ip":        get_ip(line),
        "raw":       line.strip(),
    }


def parse_file(filepath):
    events = []
    with open(filepath, "r", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(normalize_line(line))
    return events


def print_report(all_events, filepaths):
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for e in all_events:
        counts[e["severity"]] += 1

    print("\n========================================")
    print("         SIEM NORMALIZER REPORT")
    print("========================================")
    print(f"Files scanned : {len(filepaths)}")
    print(f"Total events  : {len(all_events)}")
    print(f"  CRITICAL    : {counts['critical']}")
    print(f"  HIGH        : {counts['high']}")
    print(f"  MEDIUM      : {counts['medium']}")
    print(f"  LOW         : {counts['low']}")
    print(f"  INFO        : {counts['info']}")
    print("========================================\n")

    priority_order = ["critical", "high", "medium", "low", "info"]
    shown = 0

    for level in priority_order:
        for e in all_events:
            if e["severity"] == level and shown < 20:
                print(f"[{e['severity'].upper():8}] {e['timestamp']}  src={e['source']}  ip={e['ip']}")
                print(f"           {e['raw'][:100]}")
                print()
                shown += 1

    if len(all_events) > 20:
        print(f"... and {len(all_events) - 20} more events.\n")

  


def create_demo_logs(folder):
    auth_log = os.path.join(folder, "demo_auth.log")
    firewall_log = os.path.join(folder, "demo_firewall.log")
    web_log = os.path.join(folder, "demo_web.log")

    with open(auth_log, "w") as f:
        f.write("""Mar 15 08:00:01 server sshd[100]: Failed password for root from 10.0.0.5 port 22
Mar 15 08:00:03 server sshd[100]: Failed password for root from 10.0.0.5 port 22
Mar 15 08:00:05 server sshd[100]: Accepted password for root from 10.0.0.5 port 22
Mar 15 08:10:00 server sudo[200]: user nour : TTY=pts/0 ; PWD=/home/nour ; USER=root
Mar 15 09:00:00 server sshd[300]: Invalid user admin from 192.168.1.50 port 22
Mar 15 09:00:02 server sshd[300]: Invalid user test from 192.168.1.50 port 22
""")

    with open(firewall_log, "w") as f:
        f.write("""Mar 15 08:05:00 server kernel: iptables BLOCKED IN=eth0 SRC=10.10.10.10 DST=192.168.1.1 PROTO=TCP DPT=22
Mar 15 08:05:01 server kernel: iptables ACCEPT IN=eth0 SRC=10.0.0.1 DST=192.168.1.1 PROTO=TCP DPT=80
Mar 15 08:06:00 server kernel: ufw DROP IN=eth0 SRC=5.5.5.5 DST=192.168.1.1 PROTO=TCP DPT=3389
""")

    with open(web_log, "w") as f:
        f.write("""Mar 15 09:00:00 server nginx: 10.0.0.2 - - "GET /index.html HTTP/1.1" 200
Mar 15 09:00:05 server nginx: 10.0.0.3 - - "POST /login HTTP/1.1" 401
Mar 15 09:00:10 server nginx: 10.0.0.4 - - "GET /admin HTTP/1.1" 403
""")

    print(f"Demo logs created in: {folder}")
    return [auth_log, firewall_log, web_log]


def main():
    parser = argparse.ArgumentParser(description="Normalize logs from multiple sources into one SIEM-style report")
    parser.add_argument("-f", "--files", nargs="+", help="One or more log files to parse")
    parser.add_argument("--demo", action="store_true", help="Run with demo log files")
    args = parser.parse_args()

    if args.demo:
        filepaths = create_demo_logs("/tmp")
    elif args.files:
        filepaths = args.files
    else:
        print("Please provide log files with -f or use --demo")
        return

    all_events = []
    for path in filepaths:
        events = parse_file(path)
        all_events.extend(events)

    print_report(all_events, filepaths)


if __name__ == "__main__":
    main()
