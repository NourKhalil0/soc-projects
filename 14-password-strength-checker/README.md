# 14 Password Strength Checker

  
A command line tool that scores a password based on its length, character variety, and common patterns. It tells you exactly what to fix so you can make better passwords.

![Diagram](diagram.svg)

## Features

- Scores passwords on a scale from 0 to 7
- Checks length, lowercase, uppercase, numbers, and special characters
- Detects weak patterns like repeated characters and sequential keys
- Flags passwords from a list of the most common ones
- Gives a label: WEAK, MODERATE, STRONG, or VERY STRONG
- Gives specific feedback on what to improve
- Works with a single password or in demo mode with sample inputs

## Requirements

- Python 3.8 or above
- No extra packages needed for the main script
- matplotlib is needed only to regenerate the diagram

## Installation

```bash
git clone https://github.com/NourKhalil0/soc-projects.git
cd soc-projects/14-password-strength-checker
```

## Usage

Check one password:

```bash
python3 password_checker.py --password "YourP@ssw0rd"
```

Run the built in demo with sample passwords:

```bash
python3 password_checker.py --demo
```

## Example Output

```
Password : Summer2024
Score    : 4/7
Strength : MODERATE
Feedback :
  - Decent length (8 to 11 characters)
  - Add special characters like ! @ # $

Password : C0rr3ct!H0rse#B4tt3ry
Score    : 7/7
Strength : VERY STRONG
Feedback :
  - Great length (16+ characters)
```

## What You Learn

| Topic | What it covers |
|-------|----------------|
| Password policy | What makes a password strong or weak |
| Character entropy | Why mixing character types matters |
| Common password risks | Why default and simple passwords are dangerous |
| Pattern analysis | How attackers exploit predictable patterns |
| Scoring systems | How to build a simple rule based scoring engine |


## License

MIT License

---

Part of the SOC Projects Portfolio by NourKhalil0
