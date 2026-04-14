# 19 - SSL Certificate Checker

A command line tool that checks SSL/TLS certificates for any domain. It shows you the expiry date, who issued the cert, and how many days are left. It flags certs that are close to expiring or already expired so a SOC team can act before users start seeing browser warnings.

![Diagram](./diagram.svg)

## What it checks

- Checks one or more domains at the same time
- Shows expiry date, days remaining, issuer, subject, and number of SANs
- Assigns a clear status to every domain: OK, WARNING, CRITICAL, EXPIRED, or ERROR
- Warns you if a cert expires within 30 days
- Flags critical if it expires within 7 days
- Marks it expired if the date has already passed
- Prints a summary count at the end
- Works in demo mode with no internet needed

## Requirements

- Python 3.8 or higher
- No third party libraries needed

## Installation

```bash
git clone https://github.com/NourKhalil0/soc-projects.git
cd soc-projects/19-ssl-certificate-checker
```

No pip install needed. Everything uses the Python standard library.

## Usage

Check one or more real domains:

```bash
python3 ssl_checker.py example.com google.com
```

Run demo mode with no network required:

```bash
python3 ssl_checker.py --demo
```

## Example Output

```
=== SSL Certificate Report ===

[OK]       secure.bank.com
           Expiry:  2026-12-10 (240 days left)
           Issuer:  DigiCert Inc
           Subject: secure.bank.com
           SANs:    4

[WARNING]  api.shop.com
           Expiry:  2026-05-05 (21 days left)
           Issuer:  Let's Encrypt
           Subject: api.shop.com
           SANs:    2

[CRITICAL] vpn.corp.net
           Expiry:  2026-04-18 (4 days left)
           Issuer:  Sectigo
           Subject: vpn.corp.net
           SANs:    1

[EXPIRED]  old.portal.io
           Expiry:  2026-03-01 (-44 days left)
           Issuer:  GlobalSign
           Subject: old.portal.io
           SANs:    1

[ERROR]    internal.lab - Could not connect

Summary:
  OK: 1
  WARNING: 1
  CRITICAL: 1
  EXPIRED: 1
  ERROR: 1
```

## Notes

| Skill | What it covers |
|-------|---------------|
| TLS Handshake | How SSL/TLS connects and exchanges certificates with a server |
| Certificate Parsing | Reading expiry, issuer, subject, and SANs from certificate data |
| Python ssl Module | Using the built-in ssl and socket modules with no third party libraries |
| Status Thresholds | Turning raw expiry data into actionable alert levels |
| argparse | Building CLI tools that accept multiple positional arguments and flags |

## Project Structure

```
19-ssl-certificate-checker/
    ssl_checker.py      main script
    diagram.svg         visual overview of how the tool works
    requirements.txt    no dependencies
    README.md           this file
    .gitignore          Python gitignore
```

## License

MIT

---

Part of the SOC Projects Portfolio by NourKhalil0
