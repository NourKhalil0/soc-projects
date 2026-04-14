import argparse
import ssl
# TODO: add support for checking cert chains (intermediate certs)
# currently only checks end entity cert
import socket
import datetime

def get_cert(domain):
    ctx = ssl.create_default_context()
    sock = socket.socket(socket.AF_INET)
    sock.settimeout(5.0)
    conn = ctx.wrap_socket(sock, server_hostname=domain)
    try:
        conn.connect((domain, 443))
        cert = conn.getpeercert()
        conn.close()
        return cert
    except Exception:
        return None

def cert_field(cert, section, key):
    for field in cert.get(section, []):
        for k, v in field:
            if k == key:
                return v
    return "Unknown"

def check_domain(domain):
    cert = get_cert(domain)
    if cert is None:
        return {"domain": domain, "status": "ERROR"}
    expiry = datetime.datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    days = (expiry - datetime.datetime.utcnow()).days
    if days < 0:
        status = "EXPIRED"
    elif days <= 7:
        status = "CRITICAL"
    elif days <= 30:
        status = "WARNING"
    else:
        status = "OK"
    sans = sum(1 for t, _ in cert.get("subjectAltName", []) if t == "DNS")
    return {
        "domain": domain, "status": status,
        "expiry": expiry.strftime("%Y-%m-%d"), "days": days,
        "issuer": cert_field(cert, "issuer", "organizationName"),
        "subject": cert_field(cert, "subject", "commonName"),
        "sans": sans,
    }

DEMO = [
    {"domain": "secure.bank.com", "status": "OK", "expiry": "2026-12-10", "days": 240, "issuer": "DigiCert Inc", "subject": "secure.bank.com", "sans": 4},
    {"domain": "api.shop.com", "status": "WARNING", "expiry": "2026-05-05", "days": 21, "issuer": "Let's Encrypt", "subject": "api.shop.com", "sans": 2},
    {"domain": "vpn.corp.net", "status": "CRITICAL", "expiry": "2026-04-18", "days": 4, "issuer": "Sectigo", "subject": "vpn.corp.net", "sans": 1},
    {"domain": "old.portal.io", "status": "EXPIRED", "expiry": "2026-03-01", "days": -44, "issuer": "GlobalSign", "subject": "old.portal.io", "sans": 1},
    {"domain": "internal.lab", "status": "ERROR"},
]

LABELS = {"OK": "[OK]      ", "WARNING": "[WARNING] ", "CRITICAL": "[CRITICAL]",
          "EXPIRED": "[EXPIRED] ", "ERROR": "[ERROR]   "}

def print_result(r):
    label = LABELS.get(r["status"], "[UNKNOWN] ")
    if r["status"] == "ERROR":
        print(f"{label} {r['domain']} - Could not connect")
        return
    print(f"{label} {r['domain']}")
    print(f"           Expiry:  {r['expiry']} ({r['days']} days left)")
    print(f"           Issuer:  {r['issuer']}")
    print(f"           Subject: {r['subject']}")
    print(f"           SANs:    {r['sans']}")
    print()

def main():
    parser = argparse.ArgumentParser(description="SSL Certificate Checker for SOC teams")
    parser.add_argument("domains", nargs="*", help="Domains to check")
    parser.add_argument("--demo", action="store_true", help="Run with sample data")
    args = parser.parse_args()
    if args.demo:
        results = DEMO
    elif not args.domains:
        print("Provide at least one domain or use --demo")
        return
    else:
        results = []
        for domain in args.domains:
            print(f"Checking {domain}...")
            results.append(check_domain(domain))
    print("\n=== SSL Certificate Report ===\n")
    for r in results:
        print_result(r)
    counts = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("Summary:")
    for status, count in counts.items():
        print(f"  {status}: {count}")

if __name__ == "__main__":
    main()
