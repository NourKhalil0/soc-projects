#!/usr/bin/env python3

import argparse
import re
from collections import defaultdict


FAILED_PATTERN = re.compile(
    r"(\w+\s+\d+\s[\d:]+).*Failed password for (?:invalid user )?(\S+) from ([\d.]+)"
)
INVALID_PATTERN = re.compile(
    r"(\w+\s+\d+\s[\d:]+).*Invalid user (\S+) from ([\d.]+)"
)
SUCCESS_PATTERN = re.compile(
    r"(\w+\s+\d+\s[\d:]+).*Accepted (?:password|publickey) for (\S+) from ([\d.]+)"
)


def parse_log(filepath):
    failed = defaultdict(list)
    invalid = defaultdict(list)
    success = defaultdict(list)

    with open(filepath, "r", errors="replace") as f:
        for line in f:
            m = FAILED_PATTERN.search(line)
            if m:
                ts, user, ip = m.groups()
                failed[ip].append((ts, user))

            m = INVALID_PATTERN.search(line)
            if m:
                ts, user, ip = m.groups()
                invalid[ip].append((ts, user))

            m = SUCCESS_PATTERN.search(line)
            if m:
                ts, user, ip = m.groups()
                success[ip].append((ts, user))

    return failed, invalid, success


def find_suspects(failed, invalid, success, threshold):
    suspects = []
    all_ips = set(failed.keys()) | set(invalid.keys())

    for ip in all_ips:
        total = len(failed[ip]) + len(invalid[ip])
        if total >= threshold:
            usernames = set()
            for ts, user in failed[ip] + invalid[ip]:
                usernames.add(user)
            suspects.append({
                "ip": ip,
                "total": total,
                "users": usernames,
                "success": success.get(ip, []),
            })

    suspects.sort(key=lambda x: x["total"], reverse=True)
    return suspects


def print_report(suspects, threshold):
    print("\n========================================")
    print("       BRUTE FORCE DETECTOR REPORT")
    print("========================================")
    print(f"Threshold: {threshold} failed attempts\n")

    if not suspects:
        print("No suspicious IPs found.\n")
        return

    for s in suspects:
        status = "COMPROMISED" if s["success"] else "ATTACKING"
        print(f"IP: {s['ip']}  [{status}]")
        print(f"  Failed attempts : {s['total']}")
        print(f"  Targeted users  : {', '.join(s['users'])}")
        if s["success"]:
            for ts, user in s["success"]:
                print(f"  Successful login: {ts} as {user}")
        print()

    print("========================================\n")


def create_demo_log(path):
    lines = [
        "Mar 15 08:01:10 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:12 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:14 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:16 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:18 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:20 server sshd[100]: Failed password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 08:01:22 server sshd[100]: Accepted password for root from 10.0.0.5 port 22 ssh2",
        "Mar 15 09:00:01 server sshd[200]: Failed password for admin from 192.168.1.99 port 22 ssh2",
        "Mar 15 09:00:03 server sshd[200]: Invalid user test from 192.168.1.99 port 22",
        "Mar 15 09:00:05 server sshd[200]: Invalid user guest from 192.168.1.99 port 22",
        "Mar 15 09:00:07 server sshd[200]: Failed password for ubuntu from 192.168.1.99 port 22 ssh2",
        "Mar 15 09:00:09 server sshd[200]: Invalid user oracle from 192.168.1.99 port 22",
        "Mar 15 10:00:00 server sshd[300]: Accepted publickey for nour from 10.0.0.1 port 52000 ssh2",
    ]
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"Demo log created: {path}")


def main():
    parser = argparse.ArgumentParser(description="Detect brute force attacks in SSH auth logs")
    parser.add_argument("-f", "--file", default="/var/log/auth.log", help="Path to log file")
    parser.add_argument("-t", "--threshold", type=int, default=5, help="Number of failures before flagging an IP")
    parser.add_argument("--demo", action="store_true", help="Run with a sample log file")
    args = parser.parse_args()

    if args.demo:
        demo_path = "/tmp/demo_auth.log"
        create_demo_log(demo_path)
        args.file = demo_path

    failed, invalid, success = parse_log(args.file)
    suspects = find_suspects(failed, invalid, success, args.threshold)
    print_report(suspects, args.threshold)


if __name__ == "__main__":
    main()
