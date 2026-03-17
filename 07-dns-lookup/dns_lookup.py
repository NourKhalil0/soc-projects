#!/usr/bin/env python3

import argparse
import socket
import subprocess
import sys


SUSPICIOUS_KEYWORDS = [
    "login", "secure", "verify", "update", "account",
    "banking", "paypal", "amazon", "microsoft", "apple",
    "confirm", "support", "helpdesk", "password"
]


def resolve_a(domain):
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET)
        ips = list(set(r[4][0] for r in results))
        return ips
    except socket.gaierror:
        return []


def resolve_aaaa(domain):
    try:
        results = socket.getaddrinfo(domain, None, socket.AF_INET6)
        ips = list(set(r[4][0] for r in results))
        return ips
    except socket.gaierror:
        return []


def reverse_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "No reverse DNS"


def run_dig(domain, record_type):
    try:
        result = subprocess.run(
            ["dig", "+short", record_type, domain],
            capture_output=True, text=True, timeout=5
        )
        lines = [l.strip() for l in result.stdout.strip().split("\n") if l.strip()]
        return lines
    except Exception:
        return []


def check_suspicious(domain):
    domain_lower = domain.lower()
    found = []
    for word in SUSPICIOUS_KEYWORDS:
        if word in domain_lower:
            found.append(word)
    return found


def count_subdomains(domain):
    parts = domain.split(".")
    return max(0, len(parts) - 2)


def print_report(domain, a_records, aaaa_records, mx, ns, txt, suspicious, subdomains):
    print("\n========================================")
    print("          DNS LOOKUP REPORT")
    print("========================================")
    print(f"Domain       : {domain}")
    print(f"Subdomains   : {subdomains}")
    print("========================================\n")

    print("A Records (IPv4):")
    if a_records:
        for ip in a_records:
            rev = reverse_lookup(ip)
            print(f"  {ip}  ({rev})")
    else:
        print("  None found")

    print("\nAAAA Records (IPv6):")
    if aaaa_records:
        for ip in aaaa_records:
            print(f"  {ip}")
    else:
        print("  None found")

    print("\nMX Records (Mail):")
    if mx:
        for r in mx:
            print(f"  {r}")
    else:
        print("  None found")

    print("\nNS Records (Name Servers):")
    if ns:
        for r in ns:
            print(f"  {r}")
    else:
        print("  None found")

    print("\nTXT Records:")
    if txt:
        for r in txt[:5]:
            print(f"  {r[:80]}")
    else:
        print("  None found")

    print("\n----------------------------------------")
    if suspicious:
        print(f"WARNING: Suspicious keywords found: {', '.join(suspicious)}")
        print("This domain may be used for phishing.")
    else:
        print("No suspicious keywords detected.")

    if subdomains >= 3:
        print(f"WARNING: {subdomains} subdomain levels is unusual.")

    print("========================================\n")


def main():
    parser = argparse.ArgumentParser(description="Look up DNS records for a domain")
    parser.add_argument("domain", nargs="?", help="Domain to look up")
    parser.add_argument("--demo", action="store_true", help="Run demo on example.com")
    args = parser.parse_args()

    if args.demo:
        domain = "example.com"
    elif args.domain:
        domain = args.domain.strip().lower()
    else:
        parser.print_help()
        return

    print(f"\nLooking up: {domain}")

    a_records   = resolve_a(domain)
    aaaa_records = resolve_aaaa(domain)
    mx          = run_dig(domain, "MX")
    ns          = run_dig(domain, "NS")
    txt         = run_dig(domain, "TXT")
    suspicious  = check_suspicious(domain)
    subdomains  = count_subdomains(domain)

    print_report(domain, a_records, aaaa_records, mx, ns, txt, suspicious, subdomains)


if __name__ == "__main__":
    main()
