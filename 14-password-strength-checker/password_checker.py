import argparse
import re
# common passwords list is top 1000, should probably expand this
import string

COMMON_PASSWORDS = [
    "password", "123456", "password1", "12345678", "qwerty",
    "abc123", "letmein", "monkey", "1234567890", "iloveyou",
    "admin", "welcome", "login", "passw0rd", "master"
]

def check_length(password):
    length = len(password)
    if length < 8:
        return 0, "Too short (less than 8 characters)"
    if length < 12:
        return 1, "Decent length (8 to 11 characters)"
    if length < 16:
        return 2, "Good length (12 to 15 characters)"
    return 3, "Great length (16+ characters)"

def check_character_types(password):
    score = 0
    feedback = []
    if any(c in string.ascii_lowercase for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    if any(c in string.ascii_uppercase for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    if any(c in string.digits for c in password):
        score += 1
    else:
        feedback.append("Add numbers")
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        feedback.append("Add special characters like ! @ # $")
    return score, feedback

def check_patterns(password):
    issues = []
    if re.search(r'(.)\1{2,}', password):
        issues.append("Has repeated characters (like 'aaa')")
    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        issues.append("Has sequential numbers")
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        issues.append("Has sequential letters")
    return issues

def check_common(password):
    if password.lower() in COMMON_PASSWORDS:
        return True
    return False

def get_strength_label(score):
    if score <= 2:
        return "WEAK", "#ff4444"
    if score <= 4:
        return "MODERATE", "#ffaa00"
    if score <= 6:
        return "STRONG", "#44bb44"
    return "VERY STRONG", "#00ccff"

def analyse_password(password):
    total_score = 0
    all_feedback = []
    length_score, length_msg = check_length(password)
    total_score += length_score
    all_feedback.append(length_msg)
    char_score, char_feedback = check_character_types(password)
    total_score += char_score
    all_feedback.extend(char_feedback)
    pattern_issues = check_patterns(password)
    if pattern_issues:
        total_score -= len(pattern_issues)
        all_feedback.extend(pattern_issues)
    if check_common(password):
        total_score = 0
        all_feedback.append("This is a very common password. Change it immediately.")
    total_score = max(0, total_score)
    label, color = get_strength_label(total_score)
    return total_score, label, all_feedback

def print_result(password, score, label, feedback):
    print(f"\nPassword : {password}")
    print(f"Score    : {score}/7")
    print(f"Strength : {label}")
    print("Feedback :")
    for item in feedback:
        print(f"  - {item}")

def run_demo():
    demo_passwords = [
        "abc",
        "password",
        "Summer2024",
        "Tr0ub4dor&3",
        "C0rr3ct!H0rse#B4tt3ry"
    ]
    print("=== Demo Mode ===")
    for pw in demo_passwords:
        score, label, feedback = analyse_password(pw)
        print_result(pw, score, label, feedback)
        print()

def main():
    parser = argparse.ArgumentParser(description="Check how strong a password is")
    parser.add_argument("--password", help="Password to check")
    parser.add_argument("--demo", action="store_true", help="Run with sample passwords")
    args = parser.parse_args()
    if args.demo:
        run_demo()
        return
    if args.password:
        score, label, feedback = analyse_password(args.password)
        print_result(args.password, score, label, feedback)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
