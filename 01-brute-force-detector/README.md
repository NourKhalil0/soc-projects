# 🔐 Brute Force Detector

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Category](https://img.shields.io/badge/SOC-Log%20Analysis-red)
![Level](https://img.shields.io/badge/Level-Junior%20Analyst-orange)

A command-line tool for SOC analysts to detect **SSH brute-force attacks** by parsing Linux authentication log files (`auth.log` / `secure`). Identifies suspicious IPs, targeted usernames, and flags any IPs that achieved a successful login after repeated failures — a potential indicator of compromise.

---

## 🎯 Why This Project?

Brute-force detection is one of the most common daily tasks in a SOC. This tool simulates what analysts do when triaging alerts from a SIEM — going directly to the source logs, identifying attack patterns, and flagging compromised accounts for escalation.

---

## ✨ Features

- **Threshold-based alerting** — flags IPs that exceed a configurable number of failed logins
- **Compromise detection** — highlights IPs that eventually succeeded after brute-forcing (critical finding)
- **User enumeration tracking** — shows which usernames were targeted per attacking IP
- **Colour-coded terminal output** — red for compromised, yellow for ongoing attacks, green for OK
- **Demo mode** — built-in sample log generator for testing without a real server
- **Zero dependencies** — runs on pure Python standard library

---

## 🛠 Requirements

- Python 3.7 or higher
- Access to `/var/log/auth.log` (Linux) or `/var/log/secure` (RHEL/CentOS)
- No external packages needed

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/NourKhalil0/soc-projects.git
cd soc-projects/01-brute-force-detector

# Make the script executable
chmod +x brute_force_detector.py
```

---

## 🚀 Usage

### Scan the default log file (`/var/log/auth.log`)
```bash
python3 brute_force_detector.py
```

### Scan a custom log file
```bash
python3 brute_force_detector.py -f /var/log/secure
```

### Change the detection threshold (default: 5)
```bash
python3 brute_force_detector.py -t 10
```

### Run the built-in demo (no real log needed)
```bash
python3 brute_force_detector.py --demo
```

### Full options
```
usage: brute_force_detector.py [-h] [-f FILE] [-t THRESHOLD] [--demo]

  -f, --file        Path to auth log file (default: /var/log/auth.log)
  -t, --threshold   Failed attempts before flagging an IP (default: 5)
  --demo            Generate and analyse a sample log file for testing
```

---

## 📊 Example Output

```
============================================================
   BRUTE FORCE DETECTOR — SOC Report
============================================================
  Log file  : /tmp/sample_auth.log
  Threshold : 5 failed attempts
  Generated : 2026-03-15 09:00:00
============================================================

Summary
  Total failed login attempts : 13
  Total successful logins     : 2
  Unique suspicious IPs       : 2

Suspicious IPs (sorted by failure count)
------------------------------------------------------------

  IP Address : 192.168.1.100  [COMPROMISED]
  Failures   : 6
  Targets    : root
  Successful logins detected from this IP!
    → Mar 15 08:01:24  user=root
  Last attempts:
    ✗ Mar 15 08:01:18  user=root
    ✗ Mar 15 08:01:20  user=root
    ✗ Mar 15 08:01:22  user=root

  IP Address : 10.0.0.55  [BRUTE FORCE]
  Failures   : 6
  Targets    : admin, guest, oracle, test, ubuntu
  Last attempts:
    ✗ Mar 15 08:05:07  user=test
    ✗ Mar 15 08:05:09  user=guest
    ✗ Mar 15 08:05:11  user=oracle

============================================================
Recommended Actions
  1. Block suspicious IPs at the firewall (e.g. iptables / ufw)
  2. Investigate any COMPROMISED accounts immediately
  3. Enable MFA on all SSH accounts
  4. Consider moving SSH to a non-standard port
  5. Implement Fail2Ban for automated blocking
============================================================
```

---

## 🎓 Learning Outcomes

By building and using this tool, you demonstrate:

| Skill | Description |
|-------|-------------|
| Log Analysis | Parsing and extracting IOCs from raw auth logs |
| Python Scripting | Regex, file I/O, argparse, collections |
| Threat Detection | Identifying brute-force patterns and IOCs |
| Incident Triage | Distinguishing failed attempts from successful compromises |
| SOC Workflow | Structured reporting with actionable recommendations |

---

## 🗂 Use Cases

- **Daily log review** — quick morning check for overnight brute-force activity
- **Incident response** — first step when investigating a suspected compromise
- **Threat hunting** — proactively scanning logs for attacker IP patterns
- **Security awareness** — demonstrating attack volume to stakeholders

---

## 📁 Project Structure

```
01-brute-force-detector/
├── brute_force_detector.py   # Main detection script
├── requirements.txt          # No external dependencies
├── .gitignore
└── README.md
```

---

## 🔗 Related SOC Concepts

- **MITRE ATT&CK T1110** — Brute Force
- **MITRE ATT&CK T1078** — Valid Accounts (post-compromise)
- **Fail2Ban** — Production tool that automates IP blocking
- **SIEM correlation rules** — How this logic is implemented at scale

---

## 🤝 Contributing

Pull requests are welcome! Ideas for improvement:
- Add JSON/CSV export for SIEM ingestion
- Add GeoIP lookup for attacking IPs
- Add email alerting for critical findings
- Support for Windows Event Log format

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Part of the [SOC Projects Portfolio](https://github.com/NourKhalil0/soc-projects) — daily cybersecurity projects for aspiring junior SOC analysts.*
