#!/usr/bin/env python3
"""
Brute Force Detector
====================
Analyzes authentication log files (auth.log / secure) to detect
brute-force login attempts and suspicious IP activity.

Useful for SOC analysts performing log triage and incident investigation.
"""

import argparse
import re
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path


# ── Configuration ────────────────────────────────────────────────────────────
DEFAULT_THRESHOLD  = 5   # failed attempts before flagging an IP
DEFAULT_LOG_PATH   = "/var/log/auth.log"

# Regex patterns for common log formats
PATTERNS = {
    "failed_password": re.compile(
        r"(\w+\s+\d+\s[\d:]+).*Failed password for (?:invalid user )?(\S+) from ([\d.]+)"
    ),
    "invalid_user": re.compile(
        r"(\w+\s+\d+\s[\d:]+).*Invalid user (\S+) from ([\d.]+)"
    ),
    "accepted_password": re.compile(
        r"(\w+\s+\d+\s[\d:]+).*Accepted password for (\S+) from ([\d.]+)"
    ),
    "accepted_publickey": re.compile(
        r"(\w+\s+\d+\s[\d:]+).*Accepted publickey for (\S+) from ([\d.]+)"
    ),
}

# ANSI colours
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ── Parsing ───────────────────────────────────────────────────────────────────
def parse_log(filepath: str) -> dict:
    """Parse a log file and return structured event data."""
    events = {
        "failed":   defaultdict(list),   # ip -> [(timestamp, username), ...]
        "success":  defaultdict(list),
        "invalid":  defaultdict(list),
    }

    path = Path(filepath)
    if not path.exists():
        print(f"{RED}[ERROR]{RESET} Log file not found: {filepath}")
        sys.exit(1)

    with open(filepath, "r", errors="replace") as fh:
        for line in fh:
            for pat_name, pattern in PATTERNS.items():
                match = pattern.search(line)
                if match:
                    timestamp, username, ip = match.groups()
                    if "failed" in pat_name or "invalid" in pat_name:
                        key = "failed" if "failed" in pat_name else "invalid"
                        events[key][ip].append((timestamp, username))
                    elif "accepted" in pat_name:
                        events["success"][ip].append((timestamp, username))
    return events


# ── Analysis ──────────────────────────────────────────────────────────────────
def analyse(events: dict, threshold: int) -> dict:
    """Identify suspicious IPs that exceed the failure threshold."""
    suspects = {}

    all_failed_ips = set(events["failed"]) | set(events["invalid"])

    for ip in all_failed_ips:
        failed_hits  = events["failed"].get(ip, [])
        invalid_hits = events["invalid"].get(ip, [])
        total_fails  = len(failed_hits) + len(invalid_hits)

        if total_fails >= threshold:
            # Check if IP also had a successful login (possible successful brute-force)
            successful = events["success"].get(ip, [])
            usernames  = {u for _, u in failed_hits + invalid_hits}

            suspects[ip] = {
                "total_failures": total_fails,
                "failed_attempts": failed_hits,
                "invalid_attempts": invalid_hits,
                "successful_logins": successful,
                "targeted_users": usernames,
                "compromised": len(successful) > 0,
            }

    return suspects


# ── Reporting ─────────────────────────────────────────────────────────────────
def print_report(suspects: dict, events: dict, threshold: int, logfile: str):
    """Pretty-print the analysis report to stdout."""
    total_fails   = sum(len(v) for v in events["failed"].values()) + \
                    sum(len(v) for v in events["invalid"].values())
    total_success = sum(len(v) for v in events["success"].values())

    print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}   BRUTE FORCE DETECTOR — SOC Report{RESET}")
    print(f"{CYAN}{'='*60}{RESET}")
    print(f"  Log file  : {logfile}")
    print(f"  Threshold : {threshold} failed attempts")
    print(f"  Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{CYAN}{'='*60}{RESET}\n")

    print(f"{BOLD}Summary{RESET}")
    print(f"  Total failed login attempts : {RED}{total_fails}{RESET}")
    print(f"  Total successful logins     : {GREEN}{total_success}{RESET}")
    print(f"  Unique suspicious IPs       : {RED}{len(suspects)}{RESET}\n")

    if not suspects:
        print(f"{GREEN}[OK]{RESET} No IPs exceeded the threshold of {threshold} failures.\n")
        return

    print(f"{BOLD}Suspicious IPs (sorted by failure count){RESET}")
    print("-" * 60)

    for ip, data in sorted(suspects.items(),
                            key=lambda x: x[1]["total_failures"],
                            reverse=True):
        color = RED if data["compromised"] else YELLOW
        tag   = f"{RED}[COMPROMISED]{RESET}" if data["compromised"] else f"{YELLOW}[BRUTE FORCE]{RESET}"

        print(f"\n  IP Address : {color}{BOLD}{ip}{RESET}  {tag}")
        print(f"  Failures   : {data['total_failures']}")
        print(f"  Targets    : {', '.join(sorted(data['targeted_users']))}")

        if data["successful_logins"]:
            print(f"  {RED}Successful logins detected from this IP!{RESET}")
            for ts, user in data["successful_logins"]:
                print(f"    → {ts}  user={user}")

        # Show last 3 failed attempts
        recent = (data["failed_attempts"] + data["invalid_attempts"])[-3:]
        print(f"  Last attempts:")
        for ts, user in recent:
            print(f"    ✗ {ts}  user={user}")

    print(f"\n{CYAN}{'='*60}{RESET}")
    print(f"{BOLD}Recommended Actions{RESET}")
    print("  1. Block suspicious IPs at the firewall (e.g. iptables / ufw)")
    print("  2. Investigate any COMPROMISED accounts immediately")
    print("  3. Enable MFA on all SSH accounts")
    print("  4. Consider moving SSH to a non-standard port")
    print("  5. Implement Fail2Ban for automated blocking")
    print(f"{CYAN}{'='*60}{RESET}\n")


def generate_sample_log(path: str):
    """Generate a realistic sample auth.log for testing."""
    sample = """\
Mar 15 08:01:12 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:14 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:16 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:18 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:20 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:22 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:01:24 server sshd[1234]: Accepted password for root from 192.168.1.100 port 22 ssh2
Mar 15 08:05:01 server sshd[2345]: Failed password for admin from 10.0.0.55 port 44322 ssh2
Mar 15 08:05:03 server sshd[2345]: Failed password for admin from 10.0.0.55 port 44322 ssh2
Mar 15 08:05:05 server sshd[2345]: Failed password for ubuntu from 10.0.0.55 port 44322 ssh2
Mar 15 08:05:07 server sshd[2345]: Invalid user test from 10.0.0.55 port 44322
Mar 15 08:05:09 server sshd[2345]: Invalid user guest from 10.0.0.55 port 44322
Mar 15 08:05:11 server sshd[2345]: Invalid user oracle from 10.0.0.55 port 44322
Mar 15 09:10:00 server sshd[3456]: Accepted publickey for nour from 10.0.0.10 port 52100 ssh2
Mar 15 09:15:00 server sshd[4567]: Failed password for pi from 172.16.0.200 port 22 ssh2
Mar 15 09:15:02 server sshd[4567]: Failed password for pi from 172.16.0.200 port 22 ssh2
"""
    with open(path, "w") as fh:
        fh.write(sample)
    print(f"{GREEN}[+]{RESET} Sample log created: {path}")


# ── CLI Entry Point ───────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Brute Force Detector — Analyse SSH auth logs for suspicious activity",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 brute_force_detector.py                       # scan default /var/log/auth.log
  python3 brute_force_detector.py -f /var/log/secure    # RHEL/CentOS log path
  python3 brute_force_detector.py -t 10                 # raise threshold to 10
  python3 brute_force_detector.py --demo                # run with sample log data
        """
    )
    parser.add_argument("-f", "--file",      default=DEFAULT_LOG_PATH,
                        help="Path to auth log file (default: /var/log/auth.log)")
    parser.add_argument("-t", "--threshold", type=int, default=DEFAULT_THRESHOLD,
                        help="Failed attempts before flagging an IP (default: 5)")
    parser.add_argument("--demo",            action="store_true",
                        help="Generate and analyse a sample log file for testing")
    args = parser.parse_args()

    if args.demo:
        demo_path = "/tmp/sample_auth.log"
        generate_sample_log(demo_path)
        args.file = demo_path

    print(f"{CYAN}[*]{RESET} Parsing log file: {args.file}")
    events   = parse_log(args.file)
    suspects = analyse(events, args.threshold)
    print_report(suspects, events, args.threshold, args.file)


if __name__ == "__main__":
    main()
