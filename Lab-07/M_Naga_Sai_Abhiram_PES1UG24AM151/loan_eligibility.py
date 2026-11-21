CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

def parse_income(income):
    """
    Parses and returns monthly income as an integer.
    Handles comma-separated numeric strings and strips whitespace.
    Returns None if input is invalid, negative, malformed, or non-numeric.
    """
    if income is None:
        return None
    try:
        if isinstance(income, (int, float)):
            val = int(income)
            return val if val >= 0 else None
        if not isinstance(income, str):
            return None
        cleaned = income.replace(',', '').strip()
        if not cleaned:
            return None
        val = int(cleaned)
        return val if val >= 0 else None
    except (ValueError, TypeError):
        return None

def monthly_emi(details):
    """
    Computes monthly EMI given 'principal,rate,years' as a comma-separated string.
    Returns EMI rounded to 2 decimal places.
    Returns None if input is malformed, missing fields, or contains non-positive numbers.
    """
    if not isinstance(details, str):
        return None
    try:
        parts = [p.strip() for p in details.split(',')]
        if len(parts) != 3:
            return None
        principal = float(parts[0])
        rate = float(parts[1])
        years = float(parts[2])

        if principal <= 0 or rate < 0 or years <= 0:
            return None

        n = years * 12
        if n == 0:
            return None

        if rate == 0:
            return round(principal / n, 2)

        r = rate / 1200
        factor = (1 + r) ** n
        if factor == 1:
            return round(principal / n, 2)
        emi = principal * r * factor / (factor - 1)
        return round(emi, 2)
    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return None

def pan_category(pan):
    """
    Extracts the PAN category based on the 4th character of an Indian PAN card.
    Returns the category name (e.g., 'Individual', 'Company', etc.).
    Returns None if PAN is not a string, too short, or has an unrecognized category.
    """
    if not isinstance(pan, str) or len(pan.strip()) < 4:
        return None
    char = pan.strip()[3].upper()
    return CATEGORIES.get(char, None)

def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result)

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result)

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result)

if __name__ == "__main__":
    main()
