import argparse
import json

DEMO_HEADERS = """From: support@paypa1-secure.com
To: victim@company.com
Subject: Urgent: Verify Your Account Now
Return-Path: <bounces@shady-mailer.net>
Reply-To: noreply@paypa1-secure.com
Authentication-Results: mx.company.com; spf=fail; dkim=none; dmarc=fail"""

SUSPICIOUS_WORDS = ["urgent", "verify", "suspend", "confirm", "login", "account"]


def parse_headers(raw_text):
    headers = {}
    for line in raw_text.strip().split("\n"):
        if ": " in line and not line.startswith(" "):
            key, value = line.split(": ", 1)
            headers[key] = value
    return headers


def check_auth(auth_string):
    findings = []
    if "spf=fail" in auth_string:
        findings.append("SPF failed. Sender domain may be spoofed.")
    if "dkim=none" in auth_string or "dkim=fail" in auth_string:
        findings.append("DKIM missing or failed. Email not signed.")
    if "dmarc=fail" in auth_string:
        findings.append("DMARC failed. Domain alignment broken.")
    return findings


def check_addresses(headers):
    from_addr = headers.get("From", "")
    issues = []
    if headers.get("Reply-To", "") and headers["Reply-To"] != from_addr:
        issues.append("Reply-To does not match From address.")
    if headers.get("Return-Path", "") and from_addr not in headers["Return-Path"]:
        issues.append("Return-Path does not match From address.")
    return issues


def check_subject(subject):
    found = [w for w in SUSPICIOUS_WORDS if w in subject.lower()]
    if found:
        return ["Suspicious subject words: " + ", ".join(found)]
    return []


def run_analysis(raw_text):
    headers = parse_headers(raw_text)
    findings = (check_auth(headers.get("Authentication-Results", ""))
                + check_addresses(headers) + check_subject(headers.get("Subject", "")))
    if len(findings) >= 5:
        risk = "HIGH"
    elif len(findings) >= 3:
        risk = "MEDIUM"
    elif len(findings) >= 1:
        risk = "LOW"
    else:
        risk = "CLEAN"
    return headers, findings, risk


def print_report(headers, findings, risk):
    print("=" * 50)
    print("EMAIL HEADER ANALYSIS REPORT")
    print("=" * 50)
    for key in ["From", "To", "Subject", "Return-Path", "Reply-To"]:
        print(f"  {key}: {headers.get(key, 'N/A')}")
    print()
    for i, f in enumerate(findings, 1):
        print(f"  [{i}] {f}")
    print(f"\n  Risk Level: {risk}\n" + "=" * 50)


def main():
    parser = argparse.ArgumentParser(description="Email Header Parser")
    parser.add_argument("--file", help="Path to email header text file")
    parser.add_argument("--demo", action="store_true", help="Run with demo data")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    if args.demo:
        raw = DEMO_HEADERS
    elif args.file:
        with open(args.file) as f:
            raw = f.read()
    else:
        parser.print_help()
        return
    headers, findings, risk = run_analysis(raw)
    if args.json:
        print(json.dumps({"headers": headers, "findings": findings, "risk": risk}, indent=2))
    else:
        print_report(headers, findings, risk)


if __name__ == "__main__":
    main()
