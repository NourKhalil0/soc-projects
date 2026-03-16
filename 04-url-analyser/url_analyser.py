import argparse
import re
import urllib.parse


PHISHING_KEYWORDS = [
    "login", "signin", "verify", "account", "update", "secure",
    "banking", "password", "confirm", "ebay", "paypal", "amazon",
    "apple", "microsoft", "support", "suspend", "alert", "urgent"
]

SUSPICIOUS_TLDS = [".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq", ".pw"]


def parse_url(url):
    if not url.startswith("http"):
        url = "http://" + url
    return urllib.parse.urlparse(url)


def check_ip_host(host):
    pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    return bool(re.match(pattern, host))


def count_subdomains(host):
    parts = host.split(".")
    return max(0, len(parts) - 2)


def check_suspicious_tld(host):
    for tld in SUSPICIOUS_TLDS:
        if host.endswith(tld):
            return True
    return False


def check_keywords(url_str):
    url_lower = url_str.lower()
    found = []
    for word in PHISHING_KEYWORDS:
        if word in url_lower:
            found.append(word)
    return found


def check_url_length(url_str):
    return len(url_str) > 100


def check_at_symbol(url_str):
    return "@" in url_str


def check_double_slash(path):
    return "//" in path


def analyse(url_str):
    parsed = parse_url(url_str)
    host = parsed.netloc
    path = parsed.path
    flags = []

    if check_ip_host(host):
        flags.append("IP address used instead of a domain name")

    subdomain_count = count_subdomains(host)
    if subdomain_count >= 3:
        flags.append("Too many subdomains (" + str(subdomain_count) + ")")

    if check_suspicious_tld(host):
        flags.append("Suspicious TLD detected")

    keywords = check_keywords(url_str)
    if keywords:
        flags.append("Phishing keywords found: " + ", ".join(keywords))

    if check_url_length(url_str):
        flags.append("URL is very long (" + str(len(url_str)) + " chars)")

    if check_at_symbol(url_str):
        flags.append("At symbol in URL (can hide real destination)")

    if check_double_slash(path):
        flags.append("Double slash in path")

    return flags


def print_result(url_str, flags):
    print("\nURL: " + url_str)
    print("-" * 50)
    if not flags:
        print("Result: CLEAN (no suspicious patterns found)")
    else:
        print("Result: SUSPICIOUS")
        print("Flags (" + str(len(flags)) + "):")
        for flag in flags:
            print("  [!] " + flag)
    print()


def main():
    parser = argparse.ArgumentParser(description="URL Phishing Analyser")
    parser.add_argument("--url", help="URL to analyse")
    parser.add_argument("--demo", action="store_true", help="Run with demo URLs")
    args = parser.parse_args()

    demo_urls = [
        "https://www.google.com/search?q=cats",
        "http://192.168.1.5/login/verify/account",
        "http://secure.paypal.com.account-verify.xyz/update",
        "http://login.microsoft.support.secure.tk/@phish/confirm",
    ]

    if args.demo:
        print("Running demo analysis on sample URLs...\n")
        for url in demo_urls:
            flags = analyse(url)
            print_result(url, flags)
    elif args.url:
        flags = analyse(args.url)
        print_result(args.url, flags)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
