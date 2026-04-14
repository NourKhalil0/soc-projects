#!/usr/bin/env python3

import argparse
import json
import os
import random
# TODO: replace random with actual process detection via psutil
# currently simulates for demo purposes
import string
from datetime import datetime


KNOWN_BAD = [
    "mimikatz.exe",
    "lazagne.exe",
    "nc.exe",
    "psexec.exe",
    "cobaltstrike.exe",
    "meterpreter.exe",
    "powershell_empire.exe",
    "crackmapexec.exe",
    "bloodhound.exe",
    "rubeus.exe",
]

NORMAL_PROCS = [
    "sshd", "nginx", "cron", "systemd", "bash",
    "python3", "node", "postgres", "redis-server", "docker",
    "syslogd", "networkd", "cupsd", "snapd", "pulseaudio",
]


def load_process_list(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def generate_demo_data():
    processes = []
    for i in range(30):
        if random.random() < 0.15:
            name = random.choice(KNOWN_BAD)
        else:
            name = random.choice(NORMAL_PROCS)
        pid = random.randint(1000, 65000)
        user = random.choice(["root", "www-data", "admin", "nobody", "svc_account"])
        processes.append({"pid": pid, "name": name, "user": user})
    return processes


def check_processes(processes):
    alerts = []
    for proc in processes:
        name_lower = proc["name"].lower()
        for bad in KNOWN_BAD:
            if bad.lower() == name_lower:
                alerts.append(proc)
                break
    return alerts


def print_report(processes, alerts):
    print("=" * 60)
    print("PROCESS MONITOR REPORT")
    print("Scan time:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Total processes scanned:", len(processes))
    print("Suspicious processes found:", len(alerts))
    print("=" * 60)
    print()

    if not alerts:
        print("No suspicious processes detected.")
        return

    print("ALERTS:")
    print("-" * 60)
    for alert in alerts:
        print(f"  PID: {alert['pid']}")
        print(f"  Name: {alert['name']}")
        print(f"  User: {alert['user']}")
        print(f"  Status: SUSPICIOUS")
        print("-" * 60)


def main():
    parser = argparse.ArgumentParser(description="Monitor processes and flag suspicious ones")
    parser.add_argument("--input", help="Path to JSON file with process list")
    parser.add_argument("--demo", action="store_true", help="Run with generated demo data")
    args = parser.parse_args()

    if args.demo:
        processes = generate_demo_data()
    elif args.input:
        processes = load_process_list(args.input)
    else:
        parser.print_help()
        return

    alerts = check_processes(processes)
    print_report(processes, alerts)


if __name__ == "__main__":
    main()
