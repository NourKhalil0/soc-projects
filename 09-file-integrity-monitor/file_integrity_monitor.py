#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
from datetime import datetime


BASELINE_FILE = "baseline.json"


def hash_file(path):
    sha256 = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (IOError, PermissionError):
        return None


def scan_directory(directory):
    results = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            h = hash_file(path)
            if h:
                results[path] = h
    return results


def save_baseline(data, path):
    with open(path, "w") as f:
        json.dump({"created": datetime.now().isoformat(), "files": data}, f, indent=2)


def load_baseline(path):
    with open(path, "r") as f:
        return json.load(f)["files"]


def compare(baseline, current):
    added = []
    modified = []
    deleted = []
    for path, h in current.items():
        if path not in baseline:
            added.append(path)
        elif baseline[path] != h:
            modified.append(path)
    for path in baseline:
        if path not in current:
            deleted.append(path)
    return added, modified, deleted


def print_report(added, modified, deleted, directory):
    print("\n========================================")
    print("      FILE INTEGRITY REPORT")
    print("========================================")
    print(f"Directory : {directory}")
    print(f"Added     : {len(added)}")
    print(f"Modified  : {len(modified)}")
    print(f"Deleted   : {len(deleted)}")
    print("========================================\n")

    if added:
        print("NEW FILES:")
        for f in added:
            print(f"  [+] {f}")

    if modified:
        print("\nMODIFIED FILES:")
        for f in modified:
            print(f"  [!] {f}")

    if deleted:
        print("\nDELETED FILES:")
        for f in deleted:
            print(f"  [-] {f}")

    print("\n----------------------------------------")
    if not added and not modified and not deleted:
        print("No changes detected. All files are intact.")
    else:
        total = len(added) + len(modified) + len(deleted)
        print(f"WARNING: {total} change(s) detected.")
        print("Review the files listed above.")
    print("========================================\n")


def run_demo():
    import tempfile, shutil
    tmp = tempfile.mkdtemp()
    try:
        f1 = os.path.join(tmp, "config.cfg")
        f2 = os.path.join(tmp, "server.py")
        f3 = os.path.join(tmp, "notes.txt")

        with open(f1, "w") as f: f.write("host=localhost\nport=8080\n")
        with open(f2, "w") as f: f.write("print('server')\n")
        with open(f3, "w") as f: f.write("todo: review logs\n")

        baseline = scan_directory(tmp)

        with open(f1, "w") as f: f.write("host=attacker.com\nport=4444\n")
        os.remove(f3)
        f4 = os.path.join(tmp, "backdoor.sh")
        with open(f4, "w") as f: f.write("nc -lvp 4444\n")

        current = scan_directory(tmp)
        added, modified, deleted = compare(baseline, current)

        print("\n=== DEMO MODE ===")
        print_report(added, modified, deleted, tmp)
    finally:
        shutil.rmtree(tmp)


def main():
    parser = argparse.ArgumentParser(description="Monitor files for unexpected changes")
    parser.add_argument("directory", nargs="?", help="Directory to scan")
    parser.add_argument("--baseline", metavar="PATH", default=BASELINE_FILE,
                        help="Baseline file path")
    parser.add_argument("--save", action="store_true", help="Save a new baseline")
    parser.add_argument("--demo", action="store_true", help="Run demo with simulated changes")
    args = parser.parse_args()

    if args.demo:
        run_demo()
        return

    if not args.directory:
        parser.print_help()
        return

    directory = args.directory
    print(f"\nScanning: {directory}")
    current = scan_directory(directory)

    if args.save:
        save_baseline(current, args.baseline)
        print(f"Baseline saved to {args.baseline} ({len(current)} files indexed)")
        return

    if not os.path.exists(args.baseline):
        print("No baseline found. Run with --save first to create one.")
        return

    baseline = load_baseline(args.baseline)
    added, modified, deleted = compare(baseline, current)
    print_report(added, modified, deleted, directory)


if __name__ == "__main__":
    main()
