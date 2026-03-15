#!/usr/bin/env python3

import argparse

PHASES = {
    "1-prepare": {
        "title": "Phase 1 — Prepare",
        "steps": [
            "Make sure runbooks and procedures are written down",
            "Assign roles to each team member",
            "Confirm SIEM and EDR tools are running",
            "Have a communication plan ready",
            "Keep an up to date list of all assets",
        ]
    },
    "2-detect": {
        "title": "Phase 2 — Detect",
        "steps": [
            "Check the SIEM alert queue",
            "Read the alert details carefully",
            "Decide if this is a real incident or a false positive",
            "If real, open an incident ticket",
        ]
    },
    "3-analyse": {
        "title": "Phase 3 — Analyse",
        "steps": [
            "Collect relevant log files and screenshots",
            "Build a timeline of what happened",
            "Find all IOCs (bad IPs, hashes, domains)",
            "Search IOCs in threat intelligence sources",
            "Assign a severity level to the incident",
        ]
    },
    "4-contain": {
        "title": "Phase 4 — Contain",
        "steps": [
            "Isolate infected machines from the network",
            "Block bad IPs and domains in the firewall",
            "Disable any compromised accounts",
            "Take a memory dump if needed for forensics",
            "Document every action you take",
        ]
    },
    "5-eradicate": {
        "title": "Phase 5 — Eradicate",
        "steps": [
            "Delete all malicious files found",
            "Remove any backdoors or rogue scheduled tasks",
            "Apply the security patch that was missing",
            "Change all passwords that were compromised",
            "Run a full AV and EDR scan to confirm clean",
        ]
    },
    "6-recover": {
        "title": "Phase 6 — Recover",
        "steps": [
            "Restore the system from a clean backup",
            "Test that everything works normally",
            "Reconnect the system to the network",
            "Tell users the system is back online",
            "Keep extra monitoring on for 48 hours",
        ]
    },
    "7-review": {
        "title": "Phase 7 — Post-Incident Review",
        "steps": [
            "Write a short incident report with a timeline",
            "Hold a lessons learned meeting with the team",
            "Update SIEM detection rules based on what happened",
            "Add a new runbook if this type of incident was new",
            "Train the team on anything that was missed",
        ]
    },
}


def print_phase(key):
    phase = PHASES[key]
    print(f"\n{phase['title']}")
    print("-" * 40)
    for i, step in enumerate(phase["steps"], 1):
        print(f"  [ ] {i}. {step}")
    print()


def print_all():
    print("\n========================================")
    print("    INCIDENT RESPONSE CHECKLIST")
    print("========================================")
    for key in PHASES:
        print_phase(key)
    print("========================================\n")


def main():
    parser = argparse.ArgumentParser(description="Print an incident response checklist")
    parser.add_argument("-p", "--phase", choices=PHASES.keys(), help="Show only one phase")
    parser.add_argument("--all", action="store_true", help="Show all phases")
    args = parser.parse_args()

    if args.phase:
        print_phase(args.phase)
    else:
        print_all()


if __name__ == "__main__":
    main()
