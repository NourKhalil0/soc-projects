# 🔑 Hash Identifier

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Category](https://img.shields.io/badge/SOC-Password%20Security-purple)

This tool takes a hash string and tells you what type it is, for example MD5, SHA-1 or SHA-256. It also checks if the hash matches a known weak password like "password" or "123456". SOC analysts use this when investigating breaches where password hashes have been leaked.

---

![How Hash Identification Works](diagram.png)

---

## Features

- Identifies MD5, SHA-1, SHA-224, SHA-256, SHA-384, SHA-512 and bcrypt hashes
- Warns you if the hash matches a known weak password
- Can also generate hashes from plain text so you can test it
- Demo mode runs through several sample hashes automatically
- No external packages needed

---

## Requirements

- Python 3.7 or higher
- No external packages needed

---

## Installation

```bash
git clone https://github.com/NourKhalil0/soc-projects.git
cd soc-projects/06-hash-identifier
```

---

## Usage

Identify a hash:
```bash
python3 hash_identifier.py 5f4dcc3b5aa765d61d8327deb882cf99
```

Run the demo with sample hashes:
```bash
python3 hash_identifier.py --demo
```

Generate a hash from text:
```bash
python3 hash_identifier.py --generate password sha256
```

---

## Example Output

```
========================================
         HASH IDENTIFIER REPORT
========================================
Hash     : 5f4dcc3b5aa765d61d8327deb882cf99
Length   : 32 characters
========================================

Possible type(s): MD5
WARNING: Known weak password: 'password'

========================================
         HASH IDENTIFIER REPORT
========================================
Hash     : e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Length   : 64 characters
========================================

Possible type(s): SHA-256
```

---

## What you learn

| Skill | Description |
|-------|-------------|
| Hash types | Knowing the difference between MD5, SHA-1, SHA-256 and bcrypt |
| Password security | Understanding why weak hashes are dangerous in a breach |
| Regex | Using patterns to match and classify strings |
| Forensics | Recognising hash formats found in memory dumps and log files |

---

## Project Structure

```
06-hash-identifier/
├── hash_identifier.py
├── diagram.png
├── requirements.txt
├── .gitignore
└── README.md
```

---

## License

MIT

---

*Part of the SOC Projects Portfolio by NourKhalil0*
