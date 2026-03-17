import argparse
import re
from collections import defaultdict

DEMO_LOGS = [
    "Mar 15 08:12:01 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:12:03 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:12:05 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:12:07 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:12:09 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:12:11 server sshd[1234]: Failed password for root from 192.168.1.50 port 22 ssh2",
    "Mar 15 08:15:00 server sshd[2000]: Accepted password for admin from 10.0.0.5 port 54321 ssh2",
    "Mar 15 09:00:01 server sshd[2200]: Failed password for alice from 203.0.113.10 port 12345 ssh2",
    "Mar 15 09:00:03 server sshd[2200]: Failed password for alice from 203.0.113.10 port 12345 ssh2",
    "Mar 15 09:00:05 server sshd[2200]: Failed password for alice from 203.0.113.10 port 12345 ssh2",
    "Mar 15 09:05:00 server sshd[2300]: Accepted password for alice from 10.0.0.22 port 55000 ssh2",
    "Mar 15 10:00:00 server sshd[3000]: Failed password for bob from 198.51.100.7 port 9999 ssh2",
    "Mar 15 10:30:00 server sshd[3100]: Accepted password for bob from 10.0.0.30 port 60000 ssh2",
]

FAILED_PATTERN = re.compile(r"Failed password for (\S+) from (\S+)")
SUCCESS_PATTERN = re.compile(r"Accepted password for (\S+) from (\S+)")

BRUTE_FORCE_THRESHOLD = 5


def parse_lines(lines):
    failed = defaultdict(int)
    success = defaultdict(int)
    failed_users = defaultdict(set)

    for line in lines:
        match = FAILED_PATTERN.search(line)
        if match:
            user = match.group(1)
            ip = match.group(2)
            failed[ip] += 1
            failed_users[ip].add(user)

        match = SUCCESS_PATTERN.search(line)
        if match:
            user = match.group(1)
            ip = match.group(2)
            success[ip] += 1

    return failed, success, failed_users


def print_summary(failed, success, failed_users):
    print("\n--- Auth Log Analysis Report ---\n")

    print("Failed login attempts by IP:")
    if not failed:
        print("  None found.")
    for ip in sorted(failed, key=lambda x: failed[x], reverse=True):
        users = ", ".join(sorted(failed_users[ip]))
        print(f"  {ip}: {failed[ip]} failed attempt(s) for user(s): {users}")

    print("\nSuccessful logins by IP:")
    if not success:
        print("  None found.")
    for ip in sorted(success, key=lambda x: success[x], reverse=True):
        print(f"  {ip}: {success[ip]} successful login(s)")

    print("\nSuspicious IPs (brute force threshold reached):")
    flagged = [ip for ip in failed if failed[ip] >= BRUTE_FORCE_THRESHOLD]
    if not flagged:
        print("  None detected.")
    for ip in flagged:
        print(f"  [ALERT] {ip} with {failed[ip]} failed attempts")

    print()


def read_file(path):
    with open(path, "r") as f:
        return f.readlines()


def main():
    parser = argparse.ArgumentParser(description="Analyze SSH auth logs for suspicious activity")
    parser.add_argument("--file", help="Path to auth log file")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo data")
    args = parser.parse_args()

    if args.demo:
        lines = DEMO_LOGS
    elif args.file:
        lines = read_file(args.file)
    else:
        parser.print_help()
        return

    failed, success, failed_users = parse_lines(lines)
    print_summary(failed, success, failed_users)


main()
