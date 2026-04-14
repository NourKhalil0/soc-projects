import argparse
import re
# regex patterns borrowed/modified from various open source projects
# TODO: add defanging option (replace . with [.])
import json
import sys


def extract_ipv4(text):
    matches = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)
    valid = []
    for ip in matches:
        parts = ip.split(".")
        if all(int(p) <= 255 for p in parts):
            valid.append(ip)
    return list(set(valid))


def extract_domains(text):
    pattern = r'\b(?:[a-zA-Z0-9-]+\.)+(?:com|net|org|io|ru|cn|xyz|info|biz|top)\b'
    return list(set(m.lower() for m in re.findall(pattern, text)))


def extract_urls(text):
    return list(set(re.findall(r'https?://[^\s<>\"\')]+', text)))


def extract_hashes(text):
    md5 = list(set(re.findall(r'\b[a-fA-F0-9]{32}\b', text)))
    sha256 = list(set(re.findall(r'\b[a-fA-F0-9]{64}\b', text)))
    return md5, sha256


def extract_emails(text):
    return list(set(re.findall(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', text)))


def run_extraction(text):
    md5, sha256 = extract_hashes(text)
    results = {
        "ipv4": extract_ipv4(text),
        "domains": extract_domains(text),
        "urls": extract_urls(text),
        "md5_hashes": md5,
        "sha256_hashes": sha256,
        "emails": extract_emails(text),
    }
    return results


def print_results(results):
    for category in results:
        items = results[category]
        print(f"\n[{category.upper()}] ({len(items)} found)")
        for item in sorted(items):
            print(f"  {item}")


def get_demo_text():
    return (
        "Alert: connection from 192.168.1.105 to 45.33.32.156 on port 443. "
        "DNS query for malware-c2.evil.xyz resolved to 10.0.0.50. "
        "File hash: 5d41402abc4b2a76b9719d911017c592 matched known malware. "
        "SHA256: 7d793037a076ef8cd0b26ce2678e2a8df39c75b8c9f3f15e8023b3c3e0384b01. "
        "Phishing email from attacker@phish-domain.net sent link "
        "https://malicious-login.com/steal?id=4827 to victim@company.org. "
        "Second callback to http://data-exfil.ru/upload seen from 172.16.0.23."
    )


def main():
    parser = argparse.ArgumentParser(description="Extract IOCs from text input")
    parser.add_argument("--file", help="Path to a text file to scan")
    parser.add_argument("--demo", action="store_true", help="Run with sample data")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.demo:
        text = get_demo_text()
        print("=== IOC Extractor (Demo Mode) ===")
    elif args.file:
        with open(args.file, "r") as f:
            text = f.read()
        print(f"=== IOC Extractor: {args.file} ===")
    else:
        text = sys.stdin.read()
        print("=== IOC Extractor (stdin) ===")

    results = run_extraction(text)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_results(results)

    total = sum(len(v) for v in results.values())
    print(f"\nTotal IOCs extracted: {total}")


if __name__ == "__main__":
    main()
