import argparse
import sys

THREAT_DB = {
    "185.220.101.45": {"category": "Tor Exit Node", "score": 95, "country": "DE"},
    "194.165.16.11":  {"category": "C2 Server",     "score": 98, "country": "RU"},
    "45.142.212.100": {"category": "Botnet",         "score": 92, "country": "NL"},
    "185.156.73.26":  {"category": "Scanner",        "score": 75, "country": "RO"},
    "5.188.206.26":   {"category": "Brute Force",    "score": 88, "country": "RU"},
    "192.168.1.1":    {"category": "Private Range",  "score": 0,  "country": "N/A"},
}

DEMO_IPS = [
    "185.220.101.45", "194.165.16.11", "8.8.8.8",
    "45.142.212.100", "192.168.1.1",   "1.1.1.1", "5.188.206.26",
]


def get_risk_level(score):
    if score >= 90:
        return "CRITICAL"
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    if score > 0:
        return "LOW"
    return "CLEAN"


def check_ip(ip):
    ip = ip.strip()
    if ip in THREAT_DB:
        info = THREAT_DB[ip]
        return {"ip": ip, "score": info["score"],
                "category": info["category"], "country": info["country"],
                "risk": get_risk_level(info["score"])}
    return {"ip": ip, "score": 0, "category": "No threat data",
            "country": "Unknown", "risk": "CLEAN"}


def print_result(result):
    print(f"\nIP: {result['ip']}  Risk: {result['risk']}  Score: {result['score']}/100")
    print(f"   Category: {result['category']}  Country: {result['country']}")


def load_ips_from_file(path):
    ips = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ips.append(line)
    return ips


def print_summary(results):
    total = len(results)
    flagged = [r for r in results if r["risk"] != "CLEAN"]
    print(f"\n{'=' * 42}")
    print(f"Summary: {len(flagged)} of {total} IPs flagged")
    if flagged:
        print()
        for r in flagged:
            print(f"  [{r['risk']:8}]  {r['ip']:20}  {r['category']}")


def main():
    parser = argparse.ArgumentParser(description="IP Reputation Checker")
    parser.add_argument("--ip",   help="Single IP address to check")
    parser.add_argument("--file", help="Path to a file with one IP per line")
    parser.add_argument("--demo", action="store_true", help="Run with built-in demo IPs")
    args = parser.parse_args()

    if not args.demo and not args.ip and not args.file:
        parser.print_help()
        sys.exit(1)

    ips = []
    if args.demo:
        ips = DEMO_IPS
    elif args.ip:
        ips = [args.ip]
    elif args.file:
        ips = load_ips_from_file(args.file)

    print("IP Reputation Checker")
    print("=" * 42)
    results = []
    for ip in ips:
        result = check_ip(ip)
        print_result(result)
        results.append(result)
    print_summary(results)


if __name__ == "__main__":
    main()
