import re
from pathlib import Path


def load_weak_passwords():
    """Load common weak passwords from a text file."""

    file_path = Path(__file__).with_name("weak_passwords.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return {
                line.strip().lower()
                for line in file
                if line.strip()
            }

    except FileNotFoundError:
        return {
            "password",
            "123456",
            "admin",
            "qwerty",
            "welcome"
        }


def has_sequential_pattern(password):
    """Check for four consecutive ascending or descending characters."""

    password = password.lower()

    for i in range(len(password) - 3):
        chars = password[i:i + 4]

        if all(
            ord(chars[j + 1]) - ord(chars[j]) == 1
            for j in range(3)
        ):
            return True

        if all(
            ord(chars[j + 1]) - ord(chars[j]) == -1
            for j in range(3)
        ):
            return True

    return False


def analyze_password(password):
    """Analyze password strength without storing the password."""

    weak_passwords = load_weak_passwords()

    checks = {
        "At least 12 characters": len(password) >= 12,

        "Contains uppercase letter":
            bool(re.search(r"[A-Z]", password)),

        "Contains lowercase letter":
            bool(re.search(r"[a-z]", password)),

        "Contains a number":
            bool(re.search(r"[0-9]", password)),

        "Contains special character":
            bool(re.search(r"[^A-Za-z0-9]", password)),

        "Not a common weak password":
            password.lower() not in weak_passwords,

        "No repeated characters":
            not bool(re.search(r"(.)\1\1", password)),

        "No sequential patterns":
            not has_sequential_pattern(password)
    }

    score = 0

    if checks["At least 12 characters"]:
        score += 25
    elif len(password) >= 8:
        score += 15

    if checks["Contains uppercase letter"]:
        score += 10

    if checks["Contains lowercase letter"]:
        score += 10

    if checks["Contains a number"]:
        score += 10

    if checks["Contains special character"]:
        score += 10

    if checks["Not a common weak password"]:
        score += 15

    if checks["No repeated characters"]:
        score += 10

    if checks["No sequential patterns"]:
        score += 10

    if not checks["Not a common weak password"]:
        score = min(score, 39)

    if score >= 70:
        strength = "Strong"

    elif score >= 40:
        strength = "Medium"

    else:
        strength = "Weak"

    recommendations = []

    for check, passed in checks.items():
        if not passed:
            recommendations.append(
                f"Improve: {check}"
            )

    return {
        "score": score,
        "strength": strength,
        "checks": checks,
        "recommendations": recommendations
    }


def assess_account_risk(
    mfa_enabled,
    password_reused,
    recovery_secured
):
    """Calculate account security risk."""

    risk_score = 0
    recommendations = []

    if not mfa_enabled:
        risk_score += 1
        recommendations.append(
            "Enable Multi-Factor Authentication (MFA)."
        )

    if password_reused:
        risk_score += 1
        recommendations.append(
            "Avoid reusing passwords across accounts."
        )

    if not recovery_secured:
        risk_score += 1
        recommendations.append(
            "Secure your account recovery options."
        )

    if risk_score == 0:
        risk_level = "Low"

    elif risk_score == 1:
        risk_level = "Medium"

    else:
        risk_level = "High"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendations": recommendations
    }