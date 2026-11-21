"""Parse visitor details safely for museum admission tickets."""

from datetime import date
import re


def format_visitor_name(name):
    """Return 'Surname, Given names', or empty text for invalid input."""
    if not isinstance(name, str):
        return ""
    parts = name.split()
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0].title()
    return f"{parts[-1].title()}, {' '.join(parts[:-1]).title()}"


def parse_group_ages(text):
    """Return valid ages 0 to 120; reject a malformed group as an empty list."""
    if not isinstance(text, str):
        return []
    ages = []
    for token in text.split():
        if not re.fullmatch(r"[0-9]{1,3}", token):
            return []
        age = int(token)
        if age > 120:
            return []
        ages.append(age)
    return ages


def parse_visit_date(text):
    """Return a real YYYY-MM-DD date as a tuple, or None for invalid input."""
    if not isinstance(text, str):
        return None
    cleaned = text.strip()
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", cleaned):
        return None
    try:
        visit_date = date.fromisoformat(cleaned)
    except ValueError:
        return None
    return visit_date.year, visit_date.month, visit_date.day


def main():
    """Prompt for admission details and show safely parsed values."""
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value))

    print("\n==== Running parse_group_ages ====")
    value = input(
        "Enter the ages in the group separated by spaces (e.g. 34 12 70): "
    )
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    print("Visit date (year, month, day):", parse_visit_date(value))


if __name__ == "__main__":
    main()
