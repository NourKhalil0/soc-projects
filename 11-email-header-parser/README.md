# Email Header Parser

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Category](https://img.shields.io/badge/Category-Phishing%20Detection-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A command line tool that reads raw email headers and checks them for signs of phishing. It looks at SPF, DKIM, and DMARC results, checks if the Reply-To or Return-Path addresses match the From address, and scans the subject line for suspicious keywords. Then it gives you a risk score.

![Email Header Parser Diagram](./diagram.png)

## Features

This tool parses raw email headers from a text file or from built-in demo data. It checks the Authentication-Results header for SPF, DKIM, and DMARC failures. It compares the From address against Reply-To and Return-Path to catch mismatches. It scans the subject line for common phishing keywords like "urgent," "verify," and "suspend." It scores the email as CLEAN, LOW, MEDIUM, or HIGH risk based on how many issues it finds. You can also get the results as JSON for piping into other tools.

## Requirements

You need Python 3.8 or newer. The only extra package is matplotlib, which is used to generate the diagram. The parser itself uses only standard library modules.

## Installation

```bash
git clone https://github.com/NourKhalil0/soc-projects.git
cd soc-projects/11-email-header-parser
pip install -r requirements.txt
```

## Usage

Run with demo data to see how it works:

```bash
python email_header_parser.py --demo
```

Run on your own email header file:

```bash
python email_header_parser.py --file headers.txt
```

Get JSON output:

```bash
python email_header_parser.py --demo --json
```

## Example Output

```
==================================================
EMAIL HEADER ANALYSIS REPORT
==================================================

Key Headers:
  From: support@paypa1-secure.com
  To: victim@company.com
  Subject: Urgent: Verify Your Account Now
  Return-Path: <bounces@shady-mailer.net>
  Reply-To: noreply@paypa1-secure.com

Findings (5):
  [1] SPF check failed. Sender domain may be spoofed.
  [2] DKIM missing or failed. Email not signed properly.
  [3] DMARC failed. Domain alignment is broken.
  [4] Reply-To does not match From address.
  [5] Return-Path does not match From address.

Risk Level: HIGH
==================================================
```

## What You Learn

| Skill | Description |
|-------|-------------|
| Email header structure | How email headers are organized and what each field means |
| SPF, DKIM, DMARC | The three main email authentication methods and why they matter |
| Phishing indicators | Common signs that an email is not what it claims to be |
| Address spoofing | How attackers fake the From address and how to catch it |
| CLI tool building | Using argparse to build a proper command line tool |

## Project Structure

```
11-email-header-parser/
├── email_header_parser.py
├── diagram.png
├── generate_diagram.py
├── requirements.txt
├── .gitignore
└── README.md
```

## License

MIT

---

Part of the SOC Projects Portfolio by NourKhalil0
