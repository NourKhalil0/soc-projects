#!/usr/bin/env python3

import argparse
import re
import hashlib

HASH_TYPES = [
    (32,  r"^[a-fA-F0-9]{32}$",  "MD5"),
    (40,  r"^[a-fA-F0-9]{40}$",  "SHA-1"),
    (56,  r"^[a-fA-F0-9]{56}$",  "SHA-224"),
    (64,  r"^[a-fA-F0-9]{64}$",  "SHA-256"),
    (96,  r"^[a-fA-F0-9]{96}$",  "SHA-384"),
    (128, r"^[a-fA-F0-9]{128}$", "SHA-512"),
    (32,  r"^\$1\$.{1,8}\$.{22}$",       "MD5crypt"),
    (60,  r"^\$2[aby]\$.{56}$",           "bcrypt"),
    (20,  r"^[a-fA-F0-9]{5}:[a-fA-F0-9]{35}$", "NTLM (pwdump)"),
]

WEAK_MD5 = {
    "5f4dcc3b5aa765d61d8327deb882cf99": "password",
    "e10adc3949ba59abbe56e057f20f883e": "123456",
    "25d55ad283aa400af464c76d713c07ad": "12345678",
    "d8578edf8458ce06fbc5bb76a58c5ca4": "qwerty",
    "abc123": "abc123",
}

WEAK_SHA1 = {
    "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8": "password",
    "7c4a8d09ca3762af61e59520943dc26494f8941b": "123456",
    "f7c3bc1d808e04732adf679965ccc34ca7ae3441": "1234567890",
}


def identify(hash_str):
    hash_str = hash_str.strip()
    matches = []
    for length, pattern, name in HASH_TYPES:
        if re.match(pattern, hash_str):
            matches.append(name)
    return matches


def check_weak(hash_str):
    h = hash_str.lower().strip()
    if h in WEAK_MD5:
        return f"Known weak password: '{WEAK_MD5[h]}'"
    if h in WEAK_SHA1:
        return f"Known weak password: '{WEAK_SHA1[h]}'"
    return None


def hash_string(text, algorithm):
    algorithms = {
        "md5":    hashlib.md5,
        "sha1":   hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    if algorithm not in algorithms:
        print(f"Unknown algorithm: {algorithm}")
        return
    result = algorithms[algorithm](text.encode()).hexdigest()
    print(f"\n{algorithm.upper()} hash of '{text}':")
    print(f"  {result}\n")


def print_result(hash_str, types, weak):
    print("\n========================================")
    print("         HASH IDENTIFIER REPORT")
    print("========================================")
    print(f"Hash     : {hash_str[:60]}{'...' if len(hash_str) > 60 else ''}")
    print(f"Length   : {len(hash_str)} characters")
    print("========================================\n")

    if types:
        print(f"Possible type(s): {', '.join(types)}")
    else:
        print("Could not identify this hash type.")

    if weak:
        print(f"WARNING: {weak}")

    print()


def run_demo():
    samples = [
        "5f4dcc3b5aa765d61d8327deb882cf99",
        "5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8",
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "notahash123",
    ]
    print("\n=== DEMO MODE ===\n")
    for s in samples:
        types = identify(s)
        weak  = check_weak(s)
        print_result(s, types, weak)


def main():
    parser = argparse.ArgumentParser(description="Identify hash types and check for known weak passwords")
    parser.add_argument("hash", nargs="?", help="Hash string to identify")
    parser.add_argument("--generate", nargs=2, metavar=("TEXT", "ALGO"),
                        help="Generate a hash, e.g. --generate password sha256")
    parser.add_argument("--demo", action="store_true", help="Run with sample hashes")
    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.generate:
        hash_string(args.generate[0], args.generate[1].lower())
    elif args.hash:
        types = identify(args.hash)
        weak  = check_weak(args.hash)
        print_result(args.hash, types, weak)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
