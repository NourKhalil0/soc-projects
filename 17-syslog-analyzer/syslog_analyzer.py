import argparse
import re

DEMO_LOGS = [
    "Apr 10 09:01:22 server sudo: user1 : TTY=pts/0 ; PWD=/home/user1 ; USER=root ; COMMAND=/bin/bash",
    "Apr 10 09:02:15 server kernel: [123456.789] segfault at 0 ip 00000000 error 4 in bash",
    "Apr 10 09:03:00 server sshd[1234]: Failed password for root from 192.168.1.100 port 22 ssh2",
    "Apr 10 09:03:01 server sshd[1235]: Failed password for root from 192.168.1.100 port 22 ssh2",
    "Apr 10 09:03:02 server sshd[1236]: Failed password for root from 192.168.1.100 port 22 ssh2",
    "Apr 10 09:04:00 server sshd[1237]: Accepted password for admin from 10.0.0.5 port 22 ssh2",
    "Apr 10 09:06:00 server kernel: Out of memory: Kill process 1234 (apache2) score 900",
    "Apr 10 09:07:00 server useradd[700]: new user: name=backdoor, UID=0, GID=0",
    "Apr 10 09:08:00 server sudo: user2 : TTY=pts/1 ; PWD=/tmp ; USER=root ; COMMAND=/usr/bin/wget",
]
BAD_CMDS = ["/bin/bash", "/bin/sh", "wget", "curl", "nc ", "ncat", "python", "perl"]

def parse_args():
    parser = argparse.ArgumentParser(description="Syslog Analyzer")
    parser.add_argument("--log", help="Path to syslog file")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    return parser.parse_args()

def read_log_file(path):
    with open(path, "r") as f:
        return [line.strip() for line in f]

def check_line(line):
    if "Failed password" in line:
        match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
        if match:
            return ("MEDIUM", "SSH failure from " + match.group(1))
    if "Accepted password" in line:
        match = re.search(r"for (\w+) from (\d+\.\d+\.\d+\.\d+)", line)
        if match:
            return ("INFO", "SSH login by " + match.group(1) + " from " + match.group(2))
    if "sudo:" in line and "COMMAND=" in line:
        cmd_match = re.search(r"COMMAND=(.+)$", line)
        user_match = re.search(r"sudo:\s+(\w+)\s+:", line)
        cmd = cmd_match.group(1) if cmd_match else ""
        user = user_match.group(1) if user_match else "unknown"
        for bad in BAD_CMDS:
            if bad in cmd:
                return ("HIGH", "Suspicious sudo by " + user + ": " + cmd.strip())
        return ("INFO", "Sudo by " + user + ": " + cmd.strip())
    if "new user:" in line and "UID=0" in line:
        return ("CRITICAL", "Root-level account created")
    if "new user:" in line:
        return ("MEDIUM", "New user account created")
    if "kernel:" in line:
        if "Out of memory" in line:
            return ("HIGH", "OOM killer triggered")
        if "segfault" in line:
            return ("MEDIUM", "Segfault in kernel log")
    return None

def check_brute_force(lines):
    counts = {}
    for line in lines:
        if "Failed password" in line:
            match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", line)
            if match:
                ip = match.group(1)
                counts[ip] = counts.get(ip, 0) + 1
    results = []
    for ip, count in counts.items():
        if count >= 3:
            results.append(("HIGH", "Brute force from " + ip + " (" + str(count) + " failures)"))
    return results

def print_findings(findings):
    order = ["CRITICAL", "HIGH", "MEDIUM", "INFO"]
    sorted_findings = sorted(findings, key=lambda x: order.index(x[0]) if x[0] in order else 99)
    for severity, msg in sorted_findings:
        print("[" + severity + "] " + msg)

def main():
    args = parse_args()
    if args.demo:
        lines = DEMO_LOGS
    elif args.log:
        lines = read_log_file(args.log)
    else:
        print("Use --demo or --log <path>")
        return
    print("Syslog Analyzer")
    print("=" * 40)
    print("Scanning " + str(len(lines)) + " lines...\n")
    findings = []
    for line in lines:
        result = check_line(line)
        if result:
            findings.append(result)
    findings = findings + check_brute_force(lines)
    print_findings(findings)
    print("\nTotal findings: " + str(len(findings)))

if __name__ == "__main__":
    main()
